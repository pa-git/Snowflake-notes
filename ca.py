description: >
  Execute the analysis plan using the exact filters and search query provided by the previous task. This task is not responsible for reinterpreting the plan—only for executing it exactly as received.

  **Follow these steps**:
  - Review the `analysis_plan` to understand what information to retrieve and how to process it.
  - Retrieve the required content using the contract search tool, using the `query`, `source`, `vendor`, and `section` parameters exactly as provided. Do not modify them.
  - Execute the plan as written by transforming the retrieved content into structured output such as summaries, lists, or comparison tables—strictly based on the retrieved data.

  **Important**:
  - Do not generate answers beyond what is directly supported by the retrieved content.
