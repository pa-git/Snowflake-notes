import os, json, tempfile, time, mlflow
from datetime import datetime

def _maybe_dict(x):
    try:
        if hasattr(x, "model_dump"): return x.model_dump()
        if hasattr(x, "dict"): return x.dict()
    except Exception:
        pass
    return x

def _first(*candidates):
    for c in candidates:
        if c is not None:
            return c
    return None

def crew_to_trace_safe(crew, run_inputs=None, started_at=None, finished_at=None):
    started_at = started_at or datetime.utcnow().isoformat()
    finished_at = finished_at or datetime.utcnow().isoformat()

    # --- Crew metadata (only rely on stable attrs)
    trace = {
        "crew": {
            "name": getattr(crew, "name", None),
            "process": getattr(crew, "process", None),  # e.g., Process.SEQUENTIAL/HIERARCHICAL
            "started_at": started_at,
            "finished_at": finished_at,
            "inputs": run_inputs,  # pass this from your runner
        },
        "agents": [],
        "tasks": [],
        "usage": {},
        "errors": [],
    }

    # --- Agents (robust)
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

    # --- Tasks (robust)
    for idx, t in enumerate(getattr(crew, "tasks", []) or []):
        # inputs/context (best effort)
        t_in = _first(getattr(t, "input", None), getattr(t, "inputs", None), getattr(t, "context", None))
        # outputs across versions/examples
        t_out_txt = _first(getattr(t, "output", None), getattr(t, "result", None), getattr(t, "final_output", None))
        t_json = _first(getattr(t, "output_json", None), getattr(t, "pydantic", None))
        # optional traces
        t_steps = _first(getattr(t, "intermediate_steps", None), getattr(t, "history", None), getattr(t, "log", None))
        # artifacts (if any)
        t_arts = []
        arts = getattr(t, "artifacts", None)
        if arts:
            for art in arts:
                if isinstance(art, dict):
                    t_arts.append(art)
                else:
                    t_arts.append({"name": getattr(art, "name", None), "path": getattr(art, "path", None)})

        # agent/model
        agent = getattr(t, "agent", None)
        agent_llm = getattr(agent, "llm", None)
        model_name = _first(getattr(agent_llm, "model_name", None), getattr(agent_llm, "model", None))

        # usage (only if you populated it during run)
        usage = getattr(t, "usage", None) or {}

        # capture a filtered shallow dump of unknown extras for debugging
        extras = {}
        try:
            for k, v in (getattr(t, "__dict__", {}) or {}).items():
                if k not in {"name","description","expected_output","agent","output","result","final_output",
                             "output_json","pydantic","intermediate_steps","history","log","artifacts","usage",
                             "input","inputs","context","status"}:
                    # avoid huge/referential fields
                    if isinstance(v, (str, int, float, bool, type(None), list, dict)):
                        extras[k] = v
        except Exception:
            pass

        trace["tasks"].append({
            "idx": idx,
            "name": getattr(t, "name", None),
            "agent_role": getattr(agent, "role", None),
            "description": getattr(t, "description", None),
            "expected_output": getattr(t, "expected_output", None),
            "status": getattr(t, "status", "completed"),
            "model": model_name,
            "input": _maybe_dict(t_in),
            "output_text": t_out_txt if (isinstance(t_out_txt, (str, type(None)))) else str(t_out_txt),
            "output_json": _maybe_dict(t_json),
            "intermediate_steps": _maybe_dict(t_steps),
            "artifacts": t_arts,
            "usage": usage,
            "extras": extras or None,
        })

    return trace

def log_crew_trace_to_mlflow(crew, experiment="crewai", run_name=None, run_inputs=None):
    mlflow.set_experiment(experiment)
    run_name = run_name or f"Crew-{getattr(crew,'name', 'unnamed')}-{int(time.time())}"

    started_at = datetime.utcnow().isoformat()
    trace = crew_to_trace_safe(crew, run_inputs=run_inputs, started_at=started_at)

    # aggregate simple metrics
    n_tasks = len(trace["tasks"])
    n_agents = len(trace["agents"])
    p_tokens = sum(int((t.get("usage") or {}).get("prompt_tokens", 0)) for t in trace["tasks"])
    c_tokens = sum(int((t.get("usage") or {}).get("completion_tokens", 0)) for t in trace["tasks"])

    with mlflow.start_run(run_name=run_name):
        mlflow.log_params({
            "crew_name": trace["crew"]["name"],
            "process": str(trace["crew"]["process"]),
            "num_agents": n_agents,
            "num_tasks": n_tasks,
        })
        mlflow.log_metrics({
            "prompt_tokens_total": p_tokens,
            "completion_tokens_total": c_tokens,
        })

        # write full trace + JSONL of tasks
        import tempfile, os, json
        with tempfile.TemporaryDirectory() as td:
            with open(os.path.join(td, "trace.json"), "w", encoding="utf-8") as f:
                json.dump(trace, f, ensure_ascii=False, indent=2)
            with open(os.path.join(td, "tasks.jsonl"), "w", encoding="utf-8") as f:
                for t in trace["tasks"]:
                    f.write(json.dumps(t, ensure_ascii=False) + "\n")
            mlflow.log_artifacts(td, artifact_path="crewai_trace")

        # optional: child runs per task
        for t in trace["tasks"]:
            tr_name = f"task-{t['idx']}-{t.get('name') or 'unnamed'}"
            with mlflow.start_run(run_name=tr_name, nested=True):
                mlflow.log_params({
                    "task_idx": t["idx"],
                    "task_name": t.get("name"),
                    "agent_role": t.get("agent_role"),
                    "model": t.get("model"),
                })
                with tempfile.TemporaryDirectory() as td2:
                    for fname, payload in [
                        ("input.json", t.get("input")),
                        ("output_text.txt", t.get("output_text")),
                        ("output_json.json", t.get("output_json")),
                        ("intermediate_steps.json", t.get("intermediate_steps")),
                        ("artifacts.json", t.get("artifacts")),
                        ("extras.json", t.get("extras")),
                    ]:
                        p = os.path.join(td2, fname)
                        if fname.endswith(".json"):
                            json.dump(payload, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                        else:
                            open(p, "w", encoding="utf-8").write(str(payload or ""))
                    mlflow.log_artifacts(td2, artifact_path="task_payloads")

    return trace
