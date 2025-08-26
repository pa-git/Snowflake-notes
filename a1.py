# timing_callbacks.py
import time
from collections import defaultdict
from crewai import Agent, Task, Crew, Process

# in-memory timing store keyed by task_id
_task_start = {}
_task_durations = defaultdict(float)

def step_timer(event, **kwargs):
    """
    Called after each agent step.
    We treat the first step we see for a task as the task 'start'.
    """
    task_id = getattr(event, "task_id", None) or event.get("task_id")
    if task_id and task_id not in _task_start:
        _task_start[task_id] = time.perf_counter()

def task_timer(task_output):
    """
    Called once a task completes.
    Computes and records duration.
    """
    # TaskOutput usually carries a task_id (and other metadata)
    task_id = getattr(task_output, "task_id", None) or getattr(task_output, "id", None)
    start = _task_start.pop(task_id, None)
    if start is not None:
        secs = time.perf_counter() - start
        _task_durations[task_id] = secs
        print(f"[Task {task_id}] '{task_output.description}' finished in {secs:.2f}s")
    else:
        # fallback: we didn't see steps (e.g., tool-less/one-shot), start now ~ end=now
        _task_durations[task_id] = 0.0
        print(f"[Task {task_id}] '{task_output.description}' finished (duration unknown)")

def get_task_durations():
    """Read the recorded durations (e.g., after crew.kickoff())."""
    return dict(_task_durations)

# --- Example wiring ---
if __name__ == "__main__":
    researcher = Agent(role="Researcher", goal="Find facts", backstory="...")

    t1 = Task(
        description="Find 3 recent items",
        agent=researcher,
        # you can also attach per-task callback here instead of at the Crew
        # callback=task_timer
    )

    t2 = Task(
        description="Summarize the findings",
        agent=researcher,
        context=[t1]
    )

    crew = Crew(
        agents=[researcher],
        tasks=[t1, t2],
        process=Process.sequential,
        verbose=True,
        step_callback=step_timer,   # starts the stopwatch on first step per task
        task_callback=task_timer    # stops the stopwatch when each task completes
    )

    result = crew.kickoff()
    print("Durations (s):", get_task_durations())
