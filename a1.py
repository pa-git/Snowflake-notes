def log_crew_trace_to_mlflow(
    crew,
    experiment: str = "crewai",
    run_name: str | None = None,
    run_inputs: dict | list | None = None,
    crew_result: object | None = None,
    nested_tasks: bool = True,
    crew_result_is_markdown: bool = True,   # <-- tell the logger it's MD
):
    import mlflow, os, json, tempfile
    from datetime import datetime

    mlflow.set_experiment(experiment)
    run_name = run_name or f"Crew-{getattr(crew,'name','unnamed')}-{int(datetime.utcnow().timestamp())}"

    trace = crew_to_trace_safe(
        crew,
        run_inputs=run_inputs,
        started_at=datetime.utcnow().isoformat(),
        finished_at=datetime.utcnow().isoformat(),
    )

    # Simple previews for the params table
    inputs_preview  = (str(run_inputs)[:200]  if run_inputs is not None else None)
    result_preview  = (str(crew_result)[:200] if crew_result is not None else None)

    with mlflow.start_run(run_name=run_name):
        # Params kept short
        p = {
            "crew_name": trace["crew"].get("name"),
            "process": str(trace["crew"].get("process")),
            "num_agents": len(trace["agents"]),
            "num_tasks": len(trace["tasks"]),
        }
        if inputs_preview: p["inputs_preview"] = inputs_preview
        if result_preview: p["result_preview"] = result_preview
        mlflow.log_params(p)

        # Artifacts: full trace + tasks JSONL + crew inputs + crew output (Markdown)
        with tempfile.TemporaryDirectory() as td:
            # 1) full trace
            open(os.path.join(td, "trace.json"), "w", encoding="utf-8").write(
                json.dumps(trace, ensure_ascii=False, indent=2)
            )
            # 2) tasks.jsonl
            with open(os.path.join(td, "tasks.jsonl"), "w", encoding="utf-8") as f:
                for t in trace["tasks"]:
                    f.write(json.dumps(t, ensure_ascii=False) + "\n")
            # 3) crew_inputs.json (if provided)
            if run_inputs is not None:
                open(os.path.join(td, "crew_inputs.json"), "w", encoding="utf-8").write(
                    json.dumps(run_inputs, ensure_ascii=False, indent=2, default=str)
                )
            # 4) crew result as Markdown (preferred) or JSON/text fallback
            if crew_result is not None:
                if crew_result_is_markdown and isinstance(crew_result, str):
                    # save as .md so MLflow UI shows a readable text preview
                    open(os.path.join(td, "crew_result.md"), "w", encoding="utf-8").write(crew_result)

                    # OPTIONAL: also render to HTML if you want a nicer preview in-browser
                    try:
                        import markdown as _md  # pip install markdown
                        html = _md.markdown(crew_result, extensions=["extra","tables","fenced_code"])
                        open(os.path.join(td, "crew_result.html"), "w", encoding="utf-8").write(html)
                    except Exception:
                        pass
                else:
                    # if it isn't plain MD, just dump a JSON/text version
                    try:
                        open(os.path.join(td, "crew_result.json"), "w", encoding="utf-8").write(
                            json.dumps(crew_result, ensure_ascii=False, indent=2, default=str)
                        )
                    except Exception:
                        open(os.path.join(td, "crew_result.txt"), "w", encoding="utf-8").write(str(crew_result))

            mlflow.log_artifacts(td, artifact_path="crewai_trace")

        # (nested task runs remain unchanged)
    return trace
