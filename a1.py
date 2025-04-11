data_question_intent_task:
  description: >
    Based on the metadata, the conversation history, and the user input, extract the user’s intent and provide a structured breakdown of the data request.

    This task represents a data question:
    - The user is requesting specific information that requires querying one or more tables.
    - Set `use_case_id` to 'data' and `use_case` to 'Data question'.
    - Provide a clear restatement of the user intent in `user_intent`.
    - Identify the relevant tables and columns using only what is explicitly present in the metadata.
    - Include any required joins between tables.
    - Specify any filters and aggregations mentioned or implied.

    If any part of the question is ambiguous or not covered in the metadata:
    - Use the `get_user_input` tool to ask a clarification question before proceeding.
    - NEVER make assumptions or invent table or column names.

    # Metadata
    ```{metadata}```

    # Conversation History
    ```{conversation_history}```

    # User Input
    ```{user_input}```
