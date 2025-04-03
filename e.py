identify_use_case_task:
  description: >
    # Metadata
    ```{metadata}```

    # User question
    ```{user_question}```

    # The Task
    Analyze the user question, metadata, and conversation history to determine
    which of the following three use cases it falls under:
    1) General question
    2) Data question
    3) Scenario question

    You MUST classify the user input into one of these use cases.

    If you are unable to determine the correct use case with certainty, you MUST use the `ask_question` tool
    to request clarification from the user. Continue asking clarifying questions until the use case
    can be confidently classified.

    You are NOT allowed to proceed or guess. You CANNOT complete this task without a clear and final
    classification into one of the use cases above.

    You must only use the information in the metadata and the user input.
    Never fabricate table or column names. Ask before assuming anything.
  expected_output: >
    {
      "use_case_id": "general | data | scenario",
      "use_case": "General question | Data question | Scenario question"
    }
  agent: senior_analyst
