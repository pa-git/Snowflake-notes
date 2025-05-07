Execute the analysis plan using the exact filters and search query from the previous task. Do not reinterpret or modify the plan.

**Steps**:
- Review the `analysis_plan` to understand what information to retrieve and how to process it.
- Retrieve content using the Contract Search Tool with the exact `query`, `source`, `vendor`, `division`, and `section` values provided.
- Execute the plan by transforming the retrieved content into structured output (e.g., summaries, lists, or comparison tables).

**Important**:
- Only use retrieved content. Do not infer or generate beyond it.
- Never use triple backticks (```).
- If using a Markdown table, limit to 10 columns.

**expected_output**: >
A structured Markdown response that answers the user’s question using only the retrieved data.  
Always speak directly to the user—even if the query is vague or missing.  
Respond politely and constructively. Encourage the user to follow up with more details or questions.
