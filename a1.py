# Post-hoc MLflow logger for CrewAI runs
# Works without autolog/telemetry: serialize crew/agent/task data after the run and log to MLflow.

import os
import json
import time
import tempfile
from datetime import datetime

import mlflow


# ---------- small helpers ----------

def _maybe_dict(x):
    """Convert pydantic models or objects exposing dict/model_dump to plain dicts."""
    try:
        if hasattr(x, "model_dump"):
            return x.model_dump()
        if hasattr(x, "dict"):
            return x.dict()
    except Exception:
        pass
    return x

def _first(*candidates):
    for c in candidates:
        if c is not None:
            return c
    return None

def _task_io(t):
    """
    Canonical Task outputs from TaskOutput:
      - raw (str)
      - json_dict (dict) when Task(output_json=...)
      - pydantic (model instance) when Task(output_pydantic=...)
    Returns a tuple: (text_out, json_out, pydantic_out)
    """
    out = getattr(t, "output", None)
    if out is None:
        return None, None, None

    pydantic_out = getattr(out, "pydantic", None)
    json_out = getattr(out, "json_dict", None)
    raw = getattr(out, "raw", None)

    # For a human-readable text summary: prefer structured → raw
    if pydantic_out is not None:
        text_out = str(pydantic_out)
    elif json_out is not None:
        text_out = json.dumps(json_out, ensure_ascii=False)
    else:
        text_out = raw if isinstance(raw, (str, type(None))) else str(raw)

    return text_out, json_out, pydantic_out


# ---------- core trace builders ----------

def crew_to_trace_safe(crew, run_inputs=None, started_at=None, finished_at=None):
    """
    Build a serializable trace using only stable Crew/Task attributes.
    - Crew: name, process, agents, tasks
    - Task: name, description, expected_output, agent, tools, context, markdown, etc.
    - Output: task.output.{raw,json_dict,pydantic}
    """
    started_at = started_at or datetime.utcnow().isoformat()
    finished_at = finished_at or datetime.utcnow().isoformat()

    trace = {
        "crew": {
            "name": getattr(crew, "name", None),
            "process": getattr(crew, "process", None),   # e.g., Process.SEQUENTIAL / HIERARCHICAL
            "started_at": started_at,
            "finished_at": finished_at,
            "inputs": run_inputs,                        # pass this from your kickoff wrapper
        },
        "agents": [],
        "tasks": [],
        "usage": {},    # aggregate here if you attach usage during run
        "errors": [],
    }

    # Agents (keep to stable fields; LLM model name can vary)
    for a in getattr(crew, "agents", []) or []:
        llm = getattr(a, "llm", None)
        trace["agents"].append({
            "role": getattr(a, "role", None),
            "goal": getattr(a, "goal", None),
            "backstory": getattr(a, "backstory", None),
            "llm_model": _first(getattr(llm, "model_name", None), getattr(llm, "model", None)),
            "temperature": getattr(llm, "temperature", None) if llm else None,
            "tools": [getattr(t, "name", repr(t)) for t in (getattr(a, "tools", []) or [])],
        })

    # Tasks
    for idx, t in enumerate(getattr(crew, "tasks", []) or []):
        # Inputs commonly live in one of these (context may be list of tasks/strings)
        t_input = _first(getattr(t, "input", None), getattr(t, "inputs", None), getattr(t, "context", None))

        # Canonical outputs via TaskOutput
        text_out, json_out, pyd_out = _task_io(t)
        pyd_dump = None
        if pyd_out is not None:
            if hasattr(pyd_out, "model_dump"):
                pyd_dump = pyd_out.model_dump()
            elif hasattr(pyd_out, "dict"):
                pyd_dump = pyd_out.dict()

        # Optional traces: intermediate steps/history if you attached them yourself
        t_steps = _first(getattr(t, "intermediate_steps", None), getattr(t, "history", None), getattr(t, "log", None))

        # Artifacts (best-effort)
        arts_serialized = []
        arts = getattr(t, "artifacts", None)
        if arts:
            for art in arts:
                if isinstance(art, dict):
                    arts_serialized.append(art)
                else:
                    arts_serialized.append({
                        "name": getattr(art, "name", None),
                        "path": getattr(art, "path", None)
                    })

        # Agent/model
        agent = getattr(t, "agent", None)
        agent_llm = getattr(agent, "llm", None)
        model_name = _first(getattr(agent_llm, "model_name", None), getattr(agent_llm, "model", None))

        # Usage (populate during run if you need token/cost accounting)
        usage = getattr(t, "usage", None) or {}

        # Task definition fields (aligned with Task constructor/public attrs)
        trace["tasks"].append({
            "idx": idx,
            "name": getattr(t, "name", None),
            "description": getattr(t, "description", None),
            "expected_output": getattr(t, "expected_output", None),

            "agent_role": getattr(agent, "role", None),
            "tools": [getattr(tool, "name", repr(tool)) for tool in (getattr(t, "tools", []) or [])],
            "context": t_input,   # keep raw; may be list/str

            "markdown": getattr(t, "markdown", None),
            "async_execution": getattr(t, "async_execution", None),
            "human_input": getattr(t, "human_input", None),
            "config": getattr(t, "config", None),
            "output_file": getattr(t, "output_file", None),
            "create_directory": getattr(t, "create_directory", None),
            "output_json_model": getattr(getattr(t, "output_json", None), "__name__", None),
            "output_pydantic_model": getattr(getattr(t, "output_pydantic", None), "__name__", None),
            "guardrail_max_retries": getattr(t, "guardrail_max_retries", None),

            # Outputs (canonical)
            "model": model_name,
            "input": _maybe_dict(t_input),
            "output_text": text_out,
            "output_json": _maybe_dict(json_out),
            "output_pydantic": _maybe_dict(pyd_dump),

            # Optional extras
            "intermediate_steps": _maybe_dict(t_steps),
            "artifacts": arts_serialized,
            "usage": usage,
            "status": getattr(t, "status", "completed"),
        })

    return trace


def log_crew_trace_to_mlflow(
    crew,
    experiment: str = "crewai",
    run_name: str | None = None,
    run_inputs: dict | None = None,
    nested_tasks: bool = True,
):
    """
    Create one MLflow run for the whole crew (plus optional nested runs per task).
    Artifacts:
      - crewai_trace/trace.json   (complete structured trace)
      - crewai_trace/tasks.jsonl  (one JSON line per task for easy querying)
      - crewai_trace/task_payloads/* under each child run (inputs/outputs/steps)
    """
    mlflow.set_experiment(experiment)
    run_name = run_name or f"Crew-{getattr(crew,'name', 'unnamed')}-{int(time.time())}"

    started_at = datetime.utcnow().isoformat()
    trace = crew_to_trace_safe(crew, run_inputs=run_inputs, started_at=started_at, finished_at=datetime.utcnow().isoformat())

    # Quick aggregates
    n_tasks = len(trace["tasks"])
    n_agents = len(trace["agents"])
    prompt_tokens_total = sum(int((t.get("usage") or {}).get("prompt_tokens", 0)) for t in trace["tasks"])
    completion_tokens_total = sum(int((t.get("usage") or {}).get("completion_tokens", 0)) for t in trace["tasks"])

    with mlflow.start_run(run_name=run_name):
        # Params (small, string-like)
        mlflow.log_params({
            "crew_name": trace["crew"].get("name"),
            "process": str(trace["crew"].get("process")),
            "num_agents": n_agents,
            "num_tasks": n_tasks,
        })

        # Metrics (numeric)
        mlflow.log_metrics({
            "prompt_tokens_total": prompt_tokens_total,
            "completion_tokens_total": completion_tokens_total,
        })

        # Artifacts: full trace + JSONL
        with tempfile.TemporaryDirectory() as td:
            trace_path = os.path.join(td, "trace.json")
            tasks_jsonl = os.path.join(td, "tasks.jsonl")

            with open(trace_path, "w", encoding="utf-8") as f:
                json.dump(trace, f, ensure_ascii=False, indent=2)

            with open(tasks_jsonl, "w", encoding="utf-8") as f:
                for t in trace["tasks"]:
                    f.write(json.dumps(t, ensure_ascii=False) + "\n")

            mlflow.log_artifacts(td, artifact_path="crewai_trace")

        # Optional: nested child runs per task (handy for UI filtering)
        if nested_tasks:
            for t in trace["tasks"]:
                tr_name = f"task-{t['idx']}-{t.get('name') or 'unnamed'}"
                with mlflow.start_run(run_name=tr_name, nested=True):
                    mlflow.log_params({
                        "task_idx": t["idx"],
                        "task_name": t.get("name"),
                        "agent_role": t.get("agent_role"),
                        "model": t.get("model"),
                        "output_json_model": t.get("output_json_model"),
                        "output_pydantic_model": t.get("output_pydantic_model"),
                    })
                    # Write payloads as artifacts (keep big text out of params)
                    with tempfile.TemporaryDirectory() as td2:
                        def _dump(name, payload):
                            p = os.path.join(td2, name)
                            if name.endswith(".json"):
                                with open(p, "w", encoding="utf-8") as f:
                                    json.dump(payload, f, ensure_ascii=False, indent=2)
                            else:
                                with open(p, "w", encoding="utf-8") as f:
                                    f.write("" if payload is None else str(payload))

                        _dump("input.json", t.get("input"))
                        _dump("output_text.txt", t.get("output_text"))
                        _dump("output_json.json", t.get("output_json"))
                        _dump("output_pydantic.json", t.get("output_pydantic"))
                        _dump("intermediate_steps.json", t.get("intermediate_steps"))
                        _dump("artifacts.json", t.get("artifacts"))
                        mlflow.log_artifacts(td2, artifact_path="task_payloads")

    return trace


# ---------- example usage ----------
# result = crew.kickoff(inputs={"query": "your business question"})  # or kickoff_for_each(...)
# trace = log_crew_trace_to_mlflow(crew, experiment="crewai/mycrew", run_inputs={"query": "your business question"})
# print("Logged MLflow run with", len(trace["tasks"]), "tasks.")
