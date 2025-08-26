# timing_callbacks.py
import time
import csv
from collections import defaultdict
from crewai import Agent, Task, Crew, Process

_task_start = {}
_task_durations = defaultdict(float)
CSV_FILE = "task_timings.csv"

def step_timer(event, **kwargs):
    """Mark the start time when the first step of a task begins."""
    task_id = getattr(event, "task_id", None) or event.get("task_id")
    if task_id and task_id not in _task_start:
        _task_start[task_id] = time.perf_counter()

def task_timer(task_output):
    """Compute task duration and save to CSV."""
    task_id = getattr(task_output, "task_id", None) or getattr(task_output, "id", None)
    start = _task_start.pop(task_id, None)

    if start is not None:
        duration = time.perf_counter() - start
    else:
        duration = 0.0  # fallback

    _task_durations[task_id] = duration

    # write to CSV (append mode)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # header only if file is empty
        if f.tell() == 0:
            writer.writerow(["task_id", "description", "duration_seconds"])
        writer.writerow([task_id, task_output.description, f"{duration:.2f}"])

    print(f"[Task {task_id}] '{task_output.description}' finished in {duration:.2f}s (saved to {CSV_FILE})")

def get_task_durations():
    return dict(_task_durations)

# --- Example wiring ---
if __name__ == "__main__":
    researcher = Agent(role="Researcher", goal="Find facts", backstory="...")

    t1 = Task(description="Find 3 recent items", agent=researcher)
    t2 = Task(description="Summarize findings", agent=researcher, context=[t1])

    crew = Crew(
        agents=[researcher],
        tasks=[t1, t2],
        process=Process.sequential,
        verbose=True,
        step_callback=step_timer,
        task_callback=task_timer
    )

    crew.kickoff()
    print("Durations recorded:", get_task_durations())
