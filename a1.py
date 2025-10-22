# pip install mlflow or ensure it’s available in your on-prem env
import os, json, tempfile, time, mlflow
from datetime import datetime

def _safe(obj, attr, default=None):
    return getattr(obj, attr, default)

def _maybe_dict(x):
    # Convert pydantic/BaseModels or custom objects to plain dicts
    try:
        if hasattr(x, "model_dump"):    # pydantic v2
            return x.model_dump()
        if hasattr(x, "dict"):          # pydantic v1
            return x.dict()
    except Exception:
        pass
    return x

def crew_to_trace(crew, run_inputs=None):
    """
    Convert a finished CrewAI run into a structured, serializable trace.
    Works post-hoc—no callbacks/autolog required.
    """
    started_at = _safe(crew, "started_at") or datetime.utcnow().isoformat()
    finished_at = datetime.utcnow().isoformat()

    # Top-level crew metadata (best-effort across versions)
    trace = {
        "crew": {
            "name": _safe(crew, "name"),
            "process": _safe(crew, "process"),          # e.g., "sequential"/"hierarchical"
            "verbose": _safe(crew, "verbose"),
            "started_at": started_at,
            "finished_at": finished_at,
            "inputs": run_inputs or _safe(crew, "inputs"),
        },
        "agents": [],
        "tasks": [],
        "usage": {},     # aggregate tokens/cost if you can derive them
        "errors": [],
    }

    # Agents
    agents = _safe(crew, "agents", []) or []
    for a in agents:
        trace["agents"].append({
            "role": _safe(a, "role"),
            "goal": _safe(a, "goal"),
            "backstory": _safe(a, "backstory"),
            "llm": _safe(_safe(a, "llm", None), "model_name"),
            "temperature": _safe(_safe(a, "llm", None), "temperature"),
            "tools": [ _safe(t, "name") for t in _safe(a, "tools", []) or [] ],
        })

    # Tasks (inputs, outputs, intermediate steps, artifacts)
    tasks = _safe(crew, "tasks", []) or []
    for idx, t in enumerate(tasks):
        # Common fields you can usually collect
        t_in = _safe(t, "context") or _safe(t, "input") or _safe(t, "inputs")
        t_out = _safe(t, "output") or _safe(t, "result") or _safe(t, "final_output")
        t_summary = _safe(t, "summary")
        t_json = _maybe_dict(_safe(t, "pydantic", None)) or _maybe_dict(_safe(t, "output_json", None))
        t_steps = _safe(t, "intermediate_steps") or _safe(t, "history") or _safe(t, "log")
        t_artifacts = []
        # If your tasks save artifacts (files), gather their paths if available
        if hasattr(t, "artifacts") and t.artifacts:
            for art in t.artifacts:
                # Normalize to dict
                if isinstance(art, dict):
                    t_artifacts.append(art)
                else:
                    t_artifacts.append({"name": _safe(art, "name"), "path": _safe(art, "path")})

        # Any token/usage info hanging off the task or messages
        usage = _safe(t, "usage") or {}
        model = _safe(_safe(t, "agent", None), "llm", None)
        model_name = _safe(model, "model_name")

        trace["tasks"].append({
            "idx": idx,
            "name": _safe(t, "name"),
            "agent_role": _safe(_safe(t, "agent", None), "role"),
            "description": _safe(t, "description"),
            "expected_output": _safe(t, "expected_output"),
            "status": _safe(t, "status") or "completed",
            "model": model_name,
            "input": _maybe_dict(t_in),
            "output_text": t_out if isinstance(t_out, (str, type(None))) else str(t_out),
            "output_json": _maybe_dict(t_json),
            "summary": t_summary,
            "intermediate_steps": _maybe_dict(t_steps),
            "artifacts": t_artifacts,
            "usage": usage,
        })

    return trace

def log_crew_trace_to_mlflow(
    crew, trace=None, experiment="crewai", run_name=None, run_inputs=None
):
    """
    Create one MLflow run for the whole crew + optional nested runs per task.
    Stores a JSON trace artifact and logs high-level params/metrics.
    """
    mlflow.set_experiment(experiment)
    run_name = run_name or f"Crew-{_safe(crew,'name') or 'unnamed'}-{int(time.time())}"

    if trace is None:
        trace = crew_to_trace(crew, run_inputs=run_inputs)

    # Compute some quick metrics
    num_tasks = len(trace["tasks"])
    num_agents = len(trace["agents"])
    # If you have usage info (tokens/cost), aggregate it here
    total_prompt_tokens = 0
    total_completion_tokens = 0
    for t in trace["tasks"]:
        u = t.get("usage") or {}
        total_prompt_tokens += int(u.get("prompt_tokens", 0))
        total_completion_tokens += int(u.get("completion_tokens", 0))

    with mlflow.start_run(run_name=run_name):
        # Params (string-ish, small)
        mlflow.log_params({
            "crew_name": trace["crew"].get("name"),
            "process": trace["crew"].get("process"),
            "num_agents": num_agents,
            "num_tasks": num_tasks,
        })

        # Metrics (numeric)
        mlflow.log_metrics({
            "prompt_tokens_total": total_prompt_tokens,
            "completion_tokens_total": total_completion_tokens,
        })

        # Save a rich JSON trace + per-task JSONL for easy querying
        with tempfile.TemporaryDirectory() as td:
            trace_path = os.path.join(td, "trace.json")
            tasks_path = os.path.join(td, "tasks.jsonl")

            with open(trace_path, "w", encoding="utf-8") as f:
                json.dump(trace, f, ensure_ascii=False, indent=2)

            with open(tasks_path, "w", encoding="utf-8") as f:
                for t in trace["tasks"]:
                    f.write(json.dumps(t, ensure_ascii=False) + "\n")

            mlflow.log_artifacts(td, artifact_path="crewai_trace")

        # Optionally: nested runs per task (handy for filtering in UI)
        for t in trace["tasks"]:
            tr_name = f"task-{t.get('idx')}-{t.get('name') or 'unnamed'}"
            with mlflow.start_run(run_name=tr_name, nested=True):
                mlflow.log_params({
                    "task_idx": t.get("idx"),
                    "task_name": t.get("name"),
                    "agent_role": t.get("agent_role"),
                    "model": t.get("model"),
                })
                # Small text fields as artifacts to avoid param size limits
                with tempfile.TemporaryDirectory() as td2:
                    for fname, payload in [
                        ("input.json", t.get("input")),
                        ("output_text.txt", t.get("output_text")),
                        ("output_json.json", t.get("output_json")),
                        ("intermediate_steps.json", t.get("intermediate_steps")),
                        ("artifacts.json", t.get("artifacts")),
                    ]:
                        p = os.path.join(td2, fname)
                        with open(p, "w", encoding="utf-8") as f:
                            json.dump(payload, f, ensure_ascii=False, indent=2) if fname.endswith(".json") else f.write(str(payload or ""))
                    mlflow.log_artifacts(td2, artifact_path="task_payloads")

    return trace

# --- Example usage after your run ---
# result = crew.kickoff(inputs={...})  # or however you run it on-prem
# trace = log_crew_trace_to_mlflow(crew, run_inputs={"your":"inputs"})
