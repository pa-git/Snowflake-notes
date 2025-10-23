def unpack_crew(crew, depth=2):
    """
    Print a readable summary of everything available inside a CrewAI Crew object.
    depth controls how deep to recurse (default: 2)
    """
    from pprint import pprint

    print(f"\n=== CREW SUMMARY ===")
    print(f"Name:        {getattr(crew, 'name', None)}")
    print(f"Process:     {getattr(crew, 'process', None)}")
    print(f"Verbose:     {getattr(crew, 'verbose', None)}")
    print(f"Num agents:  {len(getattr(crew, 'agents', []) or [])}")
    print(f"Num tasks:   {len(getattr(crew, 'tasks', []) or [])}")
    print("-" * 60)

    # --- Agents ---
    print("\n=== AGENTS ===")
    for i, agent in enumerate(getattr(crew, "agents", []) or []):
        print(f"\nAgent {i+1}: {getattr(agent, 'role', '(no role)')}")
        print(f"  Goal:       {getattr(agent, 'goal', '')}")
        print(f"  Backstory:  {getattr(agent, 'backstory', '')}")
        llm = getattr(agent, "llm", None)
        if llm:
            print(f"  LLM model:  {getattr(llm, 'model_name', getattr(llm, 'model', '(unknown)'))}")
            print(f"  Temperature:{getattr(llm, 'temperature', '(n/a)')}")
        tools = getattr(agent, "tools", [])
        if tools:
            print("  Tools:")
            for t in tools:
                print(f"    - {getattr(t, 'name', str(t))}")

    # --- Tasks ---
    print("\n=== TASKS ===")
    for i, task in enumerate(getattr(crew, "tasks", []) or []):
        print(f"\nTask {i+1}: {getattr(task, 'name', '(no name)')}")
        print(f"  Description:      {getattr(task, 'description', '')}")
        print(f"  Expected Output:  {getattr(task, 'expected_output', '')}")
        print(f"  Agent Role:       {getattr(getattr(task, 'agent', None), 'role', '')}")
        print(f"  Async Execution:  {getattr(task, 'async_execution', '')}")
        print(f"  Markdown:         {getattr(task, 'markdown', '')}")
        print(f"  Output JSON Model:{getattr(task, 'output_json', '')}")
        print(f"  Output Pydantic:  {getattr(task, 'output_pydantic', '')}")
        print(f"  Guardrail:        {getattr(task, 'guardrail', '')}")
        print(f"  Guardrail Retries:{getattr(task, 'guardrail_max_retries', '')}")

        # Output object if exists
        output = getattr(task, "output", None)
        if output:
            print(f"  Has Output:       ✅")
            print(f"    Raw:           {getattr(output, 'raw', '')[:200]}")
            if getattr(output, 'json_dict', None):
                print(f"    JSON keys:     {list(output.json_dict.keys())}")
            if getattr(output, 'pydantic', None):
                print(f"    Pydantic type: {type(output.pydantic).__name__}")
        else:
            print(f"  Has Output:       ❌")

        # Context or inputs
        context = getattr(task, "context", None)
        if context:
            print(f"  Context:          {context if len(str(context)) < 120 else str(context)[:120] + '...'}")

    print("\n=== OTHER ATTRIBUTES (Top Level) ===")
    # Dump other top-level attributes, excluding noisy internals
    exclude = {"agents", "tasks", "process", "name", "verbose"}
    for attr, value in crew.__dict__.items():
        if attr not in exclude:
            print(f"{attr:20}: {type(value).__name__}")

    print("\n=== END OF CREW UNPACK ===\n")
