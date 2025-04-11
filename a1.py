scenario_question_intent_task:
  description: >
    Based on the metadata, the conversation history, and the context you received, provide a structured breakdown of the scenario change(s) as described in the `restated_user_intent`.

    This task represents a scenario question:
    - The user is asking a hypothetical or “what if” question involving changes to organizational structure, headcount, or resource allocation.
    - Set `use_case_id` to 'scenario'.
    - For each change described in the input, extract the following fields to construct a `Drivers` object:
      - `transaction_type`: whether it is an increase or a decrease
      - `change_unit`: the unit used to express the change (e.g., percent, unit)
      - `change_quantity`: the numeric value of the change
      - `division`: the division impacted by the change
      - `resource_class`: the type of human resource affected (e.g., Permanent Employee, Contingent)
      - `location`: the location category where the change applies (high, medium, or low)
      - `year`: the year the change starts
      - `month`: the month the change starts

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
