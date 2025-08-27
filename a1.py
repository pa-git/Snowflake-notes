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

    # Show all attributes and values of task_output
    print("\n=== TaskOutput Debug ===")
    pprint.pprint(vars(task_output))
    print("========================\n")
    
    """Compute task duration and save to CSV."""
    task_id = getattr(task_output, "task_id", None) or getattr(task_output, "id", None)
    start = _task_start.pop(task_id, None)

    if start is not None:
        duration = time.perf_counter() - start
    else:
        duration = 0.0

    _task_durations[task_id] = duration

    # task_output.task is usually the original Task object
    task_name = getattr(task_output.task, "name", None) or "UnnamedTask"
    description = getattr(task_output, "description", "")

    # write to CSV
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # add header only if file is new
            writer.writerow(["task_id", "task_name", "description", "duration_seconds"])
        writer.writerow([task_id, task_name, description, f"{duration:.2f}"])

    print(f"[Task {task_name}] '{description}' finished in {duration:.2f}s (saved to {CSV_FILE})")

def get_task_durations():
    return dict(_task_durations)

# --- Example wiring ---
if __name__ == "__main__":
    researcher = Agent(role="Researcher", goal="Find facts", backstory="...")

    t1 = Task(name="ResearchTask", description="Find 3 recent items", agent=researcher)
    t2 = Task(name="SummaryTask", description="Summarize findings", agent=researcher, context=[t1])

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
