scenario_question_intent_task:
  description: >
    Based on the metadata, the conversation history, and the user input, extract and organize all the scenario change components.

    This task represents a scenario question:
    - The user is asking a hypothetical or “what if” question involving changes to organizational structure, headcount, or resource allocation.
    - Set `use_case_id` to 'scenario'.
    - Provide a clear restatement of the user intent in `user_intent`.
    - Identify the following for each change described in the input:
      - `change_type`: increase or decrease
      - `change_unit`: unit of measure (e.g., %, FTE)
      - `change_quantity`: numeric value of the change
      - `organization`: level affected (e.g., Division, Department, Cost Center)
      - `resources`: type of human resources involved
      - `location`: the location(s) where the change applies

    Do not proceed with assumptions. Use only what is explicitly present in the user input and metadata.

    If any required information is missing or unclear:
    - Set `use_case_id` to 'clarification'.
    - Set `clarification_question` to a clear clarification question directly addressed to the user.

    If the scenario involves multiple changes (e.g., a reduction in one area and an increase in another), create a separate `Drivers` object for each change.

    # Metadata
    ```{metadata}```

    # Conversation History
    ```{conversation_history}```

    # User Input
    ```{user_input}```
