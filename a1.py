Got it. Here's the corrected version without any icons or fluff:

---

The `ROSTER_HEADCOUNT` column contains monthly headcount snapshots. Each value represents the total number of employees at that specific point in time.

Do not use `SUM(ROSTER_HEADCOUNT)` across multiple months. This will inflate the result because the same employees are counted once for each month they appear. For example, someone employed all year would be counted 12 times.

If the goal is to get the current headcount, use only the most recent month's data. If the goal is to analyze trends, use averages or compare values month to month.
