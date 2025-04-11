general_question_task:
  description: >
    Based on the metadata, the conversation history, and the context you have, respond to the user's question as explained in the `restated_user_intent`.

    This task represents a general question:
    - No query or data retrieval is required.
    - Use only the context provided in the metadata and conversation history.
    - Set `use_case_id` to 'general' and return your response in the `answer` field.

    Do not fabricate or infer any table or column names that are not explicitly present in the metadata.

    If you are unable to provide a valid and confident answer:
    - Set `use_case_id` to 'clarification' and `use_case` to 'Clarification question'.
    - Set `clarification_question` to a clear clarification question directly addressed to the user.

    # Metadata
    ```{metadata}```

    # Conversation History
    ```{conversation_history}```

    # User Input
    ```{user_input}```
