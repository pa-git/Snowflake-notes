identify_use_case_task:
  description: >
    Analyze the metadata, conversation history, and user input to determine which of the following use cases it falls under:

    1) General question:  
    The user is asking about the structure, contents, or possibilities offered by the data.  
    In this case, use_case_id should be set to 'general', and a clear restatement of the user intent must be included.

    2) Data question:  
    The user is asking for specific information that requires querying one or more tables.  
    In this case, use_case_id should be set to 'data', and a clear restatement of the user intent must be included.

    3) Scenario question:  
    The user is asking a hypothetical or “what if” question involving changes to organizational structure, headcount, or resource allocation.  
    In this case, use_case_id should be set to 'scenario', and a clear restatement of the user intent must be included.

    4) Clarification question:  
    The user input is ambiguous or lacks sufficient information to classify.  
    In this case, use_case_id should be set to 'clarification', and a clear clarification question directly addressed to the user must be included.

    You MUST classify the user input into one of these use cases.

    If the use case is clear, you must include a restated_user_intent:  
    a plain English summary of what the user wants, written so that another agent could act on it without needing to reread the original input.

    # Metadata:
    ```{metadata}```

    # Conversation History:
    ```{conversation_history}```

    # User input:
    ```{user_input}```

  expected_output: IdentifyUsecaseTaskOutput
  agent: senior_analyst
