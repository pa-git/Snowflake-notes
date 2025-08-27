# timing_debug.py
import time
import csv
import pprint
from collections import defaultdict
from crewai import Agent, Task, Crew, Process

CSV_FILE = "task_timings.csv"

_started = {}
_durations = defaultdict(float)

def step_timer(event, **_):
    """Start stopwatch on first step, and print the raw event we get."""
    print("\n=== step_callback fired ===")
    print("Type:", type(event))
    try:
        pprint.pprint(event.__dict__)
    except Exception:
        print("Repr:", event)
    print("===========================\n")

    name = getattr(event, "name", None) or getattr(event, "task_name", None)
    if name and name not in _started:
        _started[name] = time.perf_counter()

def task_timer(task_output):
    """Stop stopwatch on completion, and print the TaskOutput we get."""
    print("\n=== task_callback fired ===")
    print("Type:", type(task_output))
    try:
        pprint.pprint(task_output.__dict__)
    except Exception:
        print("Repr:", task_output)
    print("===========================\n")

    name = getattr(task_output, "name", None) or "UnnamedTask"
    start = _started.pop(name, None)
    duration = (time.perf_counter() - start) if start is not None else 0.0
    _durations[name] = duration

    agent = getattr(task_output, "agent", "")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if f.tell() == 0:
            w.writerow(["timestamp", "task_name", "duration_seconds", "agent"])
        w.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), name, f"{duration:.2f}", agent])

    print(f"[{name}] {duration:.2f}s → logged to {CSV_FILE}")

def get_task_durations():
    return dict(_durations)

# -------- Example wiring --------
if __name__ == "__main__":
    researcher = Agent(role="Researcher", goal="Find facts", backstory="…")

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
    print("Durations:", get_task_durations())
