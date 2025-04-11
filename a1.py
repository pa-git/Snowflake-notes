general_question_task:
  description: >
    # Metadata
    ```{metadata}```

    # Conversation History
    ```{conversation_history}```

    # The Task
    Based on the metadata and the conversation history, respond directly to the user's question.

    This task represents a general question:
    - No query or data retrieval is required.
    - Use only the context provided in the metadata and conversation history.
    - Set `use_case_id` to 'general' and `use_case` to 'General question'.

    Do not fabricate or infer any table or column names that are not explicitly present in the metadata.

    If you are unable to provide a valid and confident answer:
    - Ask a clarification question directly addressed to the user.
    - In that case, set `use_case_id` to 'clarification' and `use_case` to 'Clarification question'.

  expected_output: GeneralQuestionTaskOutput
  agent: senior_analyst
