import os
from datetime import datetime
from pprint import pformat

def save_crew_summary(crew, file_path: str | None = None):
    """
    Save a complete summary of a CrewAI Crew object (agents, tasks, outputs, etc.)
    into a Markdown (.md) or text (.txt) file.

    Args:
        crew: The CrewAI Crew instance (after kickoff)
        file_path: Optional custom file path. If None, a timestamped file will be created.

    Returns:
        str: Path to the saved summary file.
    """

    if file_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"crew_summary_{getattr(crew, 'name', 'unnamed')}_{timestamp}.md"

    lines = []
    append = lines.append

    append(f"# 🧩 Crew Summary: {getattr(crew, 'name', 'Unnamed Crew')}\n")
    append(f"- **Process:** {getattr(crew, 'process', None)}")
    append(f"- **Verbose:** {getattr(crew, 'verbose', None)}")
    append(f"- **Num Agents:** {len(getattr(crew, 'agents', []) or [])}")
    append(f"- **Num Tasks:** {len(getattr(crew, 'tasks', []) or [])}")
    append("\n---\n")

    # === Agents ===
    append("## 🤖 Agents\n")
    for i, agent in enumerate(getattr(crew, "agents", []) or []):
        append(f"### Agent {i+1}: {getattr(agent, 'role', '(no role)')}")
        append(f"- **Goal:** {getattr(agent, 'goal', '')}")
        append(f"- **Backstory:** {getattr(agent, 'backstory', '')}")

        llm = getattr(agent, "llm", None)
        if llm:
            append(f"- **LLM Model:** {getattr(llm, 'model_name', getattr(llm, 'model', '(unknown)'))}")
            append(f"- **Temperature:** {getattr(llm, 'temperature', '(n/a)')}")
        tools = getattr(agent, "tools", [])
        if tools:
            append("- **Tools:**")
            for t in tools:
                append(f"  - {getattr(t, 'name', str(t))}")
        append("")

    append("\n---\n")

    # === Tasks ===
    append("## 🧠 Tasks\n")
    for i, task in enumerate(getattr(crew, "tasks", []) or []):
        append(f"### Task {i+1}: {getattr(task, 'name', '(no name)')}")
        append(f"- **Description:** {getattr(task, 'description', '')}")
        append(f"- **Expected Output:** {getattr(task, 'expected_output', '')}")
        append(f"- **Agent Role:** {getattr(getattr(task, 'agent', None), 'role', '')}")
        append(f"- **Async Execution:** {getattr(task, 'async_execution', '')}")
        append(f"- **Markdown:** {getattr(task, 'markdown', '')}")
        append(f"- **Output JSON Model:** {getattr(task, 'output_json', '')}")
        append(f"- **Output Pydantic:** {getattr(task, 'output_pydantic', '')}")
        append(f"- **Guardrail:** {getattr(task, 'guardrail', '')}")
        append(f"- **Guardrail Retries:** {getattr(task, 'guardrail_max_retries', '')}")

        output = getattr(task, "output", None)
        if output:
            append("- **Has Output:** ✅")
            raw = getattr(output, "raw", "")
            if raw:
                append(f"  - Raw Preview: {str(raw)[:300].replace('\n', ' ')}")
            json_dict = getattr(output, "json_dict", None)
            if json_dict:
                append(f"  - JSON keys: {list(json_dict.keys())}")
            pyd = getattr(output, "pydantic", None)
            if pyd:
                append(f"  - Pydantic Type: {type(pyd).__name__}")
        else:
            append("- **Has Output:** ❌")

        context = getattr(task, "context", None)
        if context:
            append(f"- **Context:** `{str(context)[:200]}`")
        append("")

    append("\n---\n")

    # === Other top-level attributes ===
    append("## ⚙️ Other Crew Attributes\n")
    exclude = {"agents", "tasks", "process", "name", "verbose"}
    for attr, value in crew.__dict__.items():
        if attr not in exclude:
            preview = pformat(value, width=80, compact=True)
            append(f"- **{attr}:** `{preview[:300]}`")

    append("\n✅ *End of Crew Summary*\n")

    # --- Write to file ---
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Crew summary saved to: {os.path.abspath(file_path)}")
    return os.path.abspath(file_path)
