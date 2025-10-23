import os
from datetime import datetime
from pprint import pformat

def _safe(obj, attr, default=None):
    try:
        return getattr(obj, attr)
    except Exception:
        return default

def _preview(val, limit=300):
    try:
        s = str(val)
    except Exception:
        s = repr(val)
    s = s.replace("\n", " ").replace("\r", " ")
    return s[:limit]

def save_crew_summary(crew, file_path=None):
    """
    Save a readable summary of a CrewAI Crew (agents, tasks, outputs) to a .md file.
    Returns the absolute path to the saved file.
    """
    if file_path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = _safe(crew, "name", "unnamed")
        file_path = f"crew_summary_{name}_{ts}.md"

    lines = []
    lines.append(f"# Crew Summary: {_safe(crew, 'name', 'Unnamed Crew')}")
    lines.append("")
    lines.append(f"- **Process:** {_safe(crew, 'process', None)}")
    lines.append(f"- **Verbose:** {_safe(crew, 'verbose', None)}")

    agents = _safe(crew, "agents", []) or []
    tasks  = _safe(crew, "tasks", []) or []
    lines.append(f"- **Num Agents:** {len(agents)}")
    lines.append(f"- **Num Tasks:** {len(tasks)}")
    lines.append("\n---\n")

    # Agents
    lines.append("## Agents")
    if not agents:
        lines.append("- (none)")
    for i, a in enumerate(agents, 1):
        lines.append(f"### Agent {i}: {_safe(a, 'role', '(no role)')}")
        lines.append(f"- **Goal:** {_safe(a, 'goal', '')}")
        lines.append(f"- **Backstory:** {_safe(a, 'backstory', '')}")

        llm = _safe(a, "llm", None)
        if llm is not None:
            model = _safe(llm, "model_name", None) or _safe(llm, "model", None)
            lines.append(f"- **LLM Model:** {model}")
            lines.append(f"- **Temperature:** {_safe(llm, 'temperature', '(n/a)')}")

        tools = _safe(a, "tools", []) or []
        if tools:
            lines.append("- **Tools:**")
            for t in tools:
                tname = _safe(t, "name", None) or _preview(t, 80)
                lines.append(f"  - {tname}")
        lines.append("")

    lines.append("\n---\n")

    # Tasks
    lines.append("## Tasks")
    if not tasks:
        lines.append("- (none)")
    for i, t in enumerate(tasks, 1):
        lines.append(f"### Task {i}: {_safe(t, 'name', '(no name)')}")
        lines.append(f"- **Description:** {_safe(t, 'description', '')}")
        lines.append(f"- **Expected Output:** {_safe(t, 'expected_output', '')}")
        agent = _safe(t, "agent", None)
        lines.append(f"- **Agent Role:** {_safe(agent, 'role', '')}")
        lines.append(f"- **Async Execution:** {_safe(t, 'async_execution', '')}")
        lines.append(f"- **Markdown:** {_safe(t, 'markdown', '')}")
        lines.append(f"- **Output JSON Model:** {_safe(t, 'output_json', '')}")
        lines.append(f"- **Output Pydantic:** {_safe(t, 'output_pydantic', '')}")
        lines.append(f"- **Guardrail:** {_safe(t, 'guardrail', '')}")
        lines.append(f"- **Guardrail Retries:** {_safe(t, 'guardrail_max_retries', '')}")

        # Output (TaskOutput with .raw / .json_dict / .pydantic)
        out = _safe(t, "output", None)
        if out is not None:
            lines.append("- **Has Output:** yes")
            raw = _safe(out, "raw", None)
            if raw is not None:
                raw_prev = _preview(raw, 300)
                lines.append(f"  - Raw Preview: {raw_prev}")
            j = _safe(out, "json_dict", None)
            if j:
                try:
                    keys = list(j.keys())
                except Exception:
                    keys = []
                lines.append(f"  - JSON keys: {keys}")
            pyd = _safe(out, "pydantic", None)
            if pyd is not None:
                lines.append(f"  - Pydantic Type: {type(pyd).__name__}")
        else:
            lines.append("- **Has Output:** no")

        # Context / inputs
        ctx = _safe(t, "context", None)
        if ctx is not None:
            lines.append(f"- **Context:** `{_preview(ctx, 200)}`")
        lines.append("")

    lines.append("\n---\n")

    # Other top-level attributes (shallow)
    lines.append("## Other Crew Attributes")
    exclude = {"agents", "tasks", "process", "name", "verbose"}
    try:
        items = list(getattr(crew, "__dict__", {}).items())
    except Exception:
        items = []
    for k, v in items:
        if k in exclude:
            continue
        prev = _preview(pformat(v, width=80, compact=True), 300)
        lines.append(f"- **{k}:** `{prev}`")

    lines.append("\n*End of Crew Summary*\n")

    # Write file
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return os.path.abspath(file_path)
