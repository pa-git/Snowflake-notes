build_execute_query:
  description: >
    # Metadata
    ```{metadata}```

    # User intent
    ```{user_intent}```

    Using the provided metadata and user intent, construct a valid {dialect} SELECT SQL query and execute it using the `execute_query` tool.

    This task requires you to:
    - Generate only SELECT queries.
    - Never return the SQL query in your response.
    - Always return the results **from the `execute_query` tool** as a **Markdown table** (without using triple backticks).

    ## Step-by-step instructions:
    1. Read and understand the metadata.
    2. Understand the user intent provided above.
    3. Determine whether joins are needed, and specify the correct type (e.g., INNER JOIN, LEFT JOIN).
    4. Identify filters to apply — only use valid filter values found in the metadata.
    5. Choose which columns to include in the SELECT clause.
    6. Assemble the complete SQL query.
    7. Execute the query using the `execute_query` tool.

    ## Query construction rules:
    - ALWAYS include both schema and table names in the format `SCHEMA.TABLE` (e.g., `SELECT * FROM SALES.ORDERS`).
    - NEVER invent table or column names not found in the metadata.
    - NEVER include the SQL query in your response — only return the query result using the `execute_query` tool.

    ## After running the query:
    - If the query returns results, format and return them as a Markdown table (no backticks).
    - If the query fails, revise the query and retry.
    - If the query cannot be constructed, respond with a clear clarification question addressed to the user.

  expected_output: A Markdown table. Do not include triple backticks (` ``` ` or ` ```markdown `) in your response.
  agent: query_builder_executor
