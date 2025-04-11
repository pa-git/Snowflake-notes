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

    ## Restated Intent
    Your output must include a field called `restated_user_intent`, which clearly summarizes the user's intent with all necessary context for downstream processing.

    - Be specific and concise.
    - Avoid vague phrasing.
    - Include only verifiable details from the input.
    - If clarification is needed, restate what is known so far and flag what is missing.

    ### Example:
    restated_user_intent: >
      The user wants to know which customer segments have seen the highest year-over-year increase in average purchase value. 
      They are specifically interested in data from the past 12 months, broken down by customer age group and location.

    You must only use the information in the metadata and the user input.  
    Never fabricate table or column names. Ask before assuming anything.

  expected_output: IdentifyUsecaseTaskOutput
  agent: senior_analyst
