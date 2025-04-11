identify_use_case_task:
  description: >
    # Metadata
    ```{metadata}```

    # Conversation History
    ```{conversation_history}```

    # User input
    ```{user_input}```

    # The Task
    Analyze the user input, metadata, and conversation history to determine which of the following use cases it falls under:

    1) General question  
       - use_case_id: 'general'  
       - use_case: 'General question'

    2) Data question  
       - use_case_id: 'data'  
       - use_case: 'Data question'

    3) Scenario question  
       - use_case_id: 'scenario'  
       - use_case: 'Scenario question'

    4) Clarification question  
       - use_case_id: 'clarification'  
       - use_case: 'Clarification question'

    You MUST classify the user input into one of these use cases.

    If you are unable to determine the correct use case with certainty, respond with a clarification question addressed directly to the user.

    You are NOT allowed to proceed or guess. You CANNOT complete this task without a clear and final classification into one of the use cases above.

    You must only use the information in the metadata and the user input.  
    Never fabricate table or column names. Ask before assuming anything.
  
  expected_output: IdentifyUsecaseTaskOutput
  agent: senior_analyst
