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

        # Optional traces: intermediate steps/history if yo
