import mlflow

mlflow.set_experiment("AnalystCrew")

with mlflow.start_run(run_name="crew-run"):
    with mlflow.start_span("crew.kickoff") as span:
        span.set_inputs({"inputs": inputs})
        result = crew.kickoff(inputs=inputs)
        span.set_outputs({"result_preview": str(result)[:200]})

    # per-task spans (example)
    for task in crew.tasks:
        with mlflow.start_span(f"task:{task.name}") as s:
            s.set_inputs({"agent": getattr(task.agent, "role", None)})
            s.set_outputs({"duration_ms": getattr(task, "execution_duration", None)})
