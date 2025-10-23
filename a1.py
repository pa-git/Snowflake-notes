with mlflow.start_run(run_name=run_name) as parent:
    # crew-level logging...

    for idx, task in enumerate(crew.tasks):
        tr_name = f"task-{idx}-{getattr(task, 'name', 'unnamed')}"
        with mlflow.start_run(run_name=tr_name, nested=True):
            dur_ms = _to_ms(getattr(task, "execution_duration", None))
            if dur_ms is not None:
                mlflow.log_metric("duration_ms", dur_ms)
                # optional: also store seconds
                mlflow.log_metric("duration_s", round(dur_ms / 1000.0, 3))
