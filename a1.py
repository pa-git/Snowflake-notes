identify_use_case_task:
  description: >
    # The Task
    You are an analyst tasked with identifying the type of question a user is asking.

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

    You are NOT allowed to guess or proceed without a clear classification.

    # Metadata
    ```{metadata}```

    # Conversation History
    ```{conversation_history}```

    # User input
    ```{user_input}```

    # Additional Requirement: restated_user_intent
    You must include a field called `restated_user_intent`.

    This is a plain English summary of what the user wants, written in a way that another agent could use without needing to reread the original question.

    Guidelines:
    - Be specific and concise.
    - Include only what is verifiable from metadata or user input.
    - If the input is unclear, explain what is known and what needs clarification.

    ## Example:
    restated_user_intent: >
      The user wants to know which customer segments have seen the highest year-over-year increase in average purchase value. 
      They are specifically interested in data from the past 12 months, broken down by customer age group and location.

  expected_output: IdentifyUsecaseTaskOutput
  agent: senior_analyst
