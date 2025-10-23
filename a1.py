for t in trace["tasks"]:
    tr_name = f"task-{t['idx']}-{t.get('name') or 'unnamed'}"
    with mlflow.start_run(run_name=tr_name, nested=True):
        # get the real Task object, not the trace dict
        task_obj = crew.tasks[t["idx"]]

        # convert to milliseconds (handles seconds/ms/timedelta)
        dur = getattr(task_obj, "execution_duration", None)
        dur_ms = _to_ms(dur)  # use the helper you defined

        if dur_ms is not None:
            mlflow.log_metric("duration_ms", dur_ms)
            mlflow.log_metric("duration_s", round(dur_ms / 1000.0, 3))
