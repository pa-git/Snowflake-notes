import csv
import time
import os

def save_task_durations_to_csv(crew):
    # Unique filename: task_durations_YYYY-MM-DD_HH-MM-SS.csv
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"task_durations_{timestamp}.csv"

    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "time", "task_name", "duration_seconds"])

        for task in crew.tasks:
            duration = task.execution_duration
            if duration is not None:
                date_str = time.strftime("%Y-%m-%d")
                time_str = time.strftime("%H:%M:%S")
                writer.writerow([date_str, time_str, task.name, f"{duration:.2f}"])

    print(f"Saved task durations to: {filename}")
