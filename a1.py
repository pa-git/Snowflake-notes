# timing_chain_from_previous_end_unique_file.py
import time
import csv
from collections import defaultdict
from crewai import Agent, Task, Crew, Process

# Build unique filename with date + time
RUN_ID = time.strftime("%Y-%m-%d_%H-%M-%S")
CSV_FILE = f"task_timings_{RUN_ID}.csv"

# --- State ---
CREW_START = None
TASK_ORDER = []             # list[str] in execution order
TASK_INDEX = {}             # name -> index
STARTED_AT = {}             # name -> perf_counter() start
ENDED_AT = {}               # name -> perf_counter() end
DURATIONS = defaultdict(float)

def init_task_order(tasks):
    """Capture task order (for Process.sequential)."""
    global TASK_ORDER, TASK_INDEX
    TASK_ORDER = [t.name or "UnnamedTask" for t in tasks]
    TASK_INDEX = {name: i for i, name in enumerate(TASK_ORDER)}

def _now_date_time():
    """Return (YYYY-MM-DD, HH:MM:SS)."""
    lt = time.localtime()
    return (
        time.strftime("%Y-%m-%d", lt),
        time.strftime("%H:%M:%S", lt),
    )

def task_timer(task_output):
    """Called once per task on completion. Logs to unique dated CSV file."""
    global ENDED_AT, STARTED_AT

    name = getattr(task_output, "name", None) or "UnnamedTask"
    now_perf = time.perf_counter()
    ENDED_AT[name] = now_perf

    # Determine start time
    if name in STARTED_AT:
        start_perf = STARTED_AT[name]
    else:
        idx = TASK_INDEX.get(name, 0)
        if idx == 0:
            start_perf = CREW_START or now_perf
        else:
            prev_name = TASK_ORDER[idx - 1]
            start_perf = ENDED_AT.get(prev_name, CREW_START or now_perf)
        STARTED_AT[name] = start_perf

    duration = max(0.0, now_perf - start_perf)
    DURATIONS[name] = duration

    agent = getattr(task_output, "agent", "")
    date_str, time_str = _now_date_time()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if f.tell() == 0:
            w.writerow(["date", "time", "task_name", "duration_seconds", "agent"])
        w.writerow([date_str, time_str, name, f"{duration:.2f}", agent])

    print(f"[{name}] {duration:.2f}s → logged to {CSV_FILE}")

def get_task_durations():
    return dict(DURATIONS)

# --- Example wiring (sequential) ---
if __name__ == "__main__":
    researcher = Agent(role="Researcher", goal="Find facts", backstory="…")

    t1 = Task(name="ResearchTask", description="Find 3 recent items", agent=researcher)
    t2 = Task(name="SummaryTask", description="Summarize findings", agent=researcher, context=[t1])

    crew = Crew(
        agents=[researcher],
        tasks=[t1, t2],
        process=Process.sequential,
        verbose=True,
        task_callback=task_timer
    )

    # Initialize order & crew start just before kickoff
    init_task_order(crew.tasks)
    CREW_START = time.perf_counter()

    crew.kickoff()
    print("Durations:", get_task_durations())
