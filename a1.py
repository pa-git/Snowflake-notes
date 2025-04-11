identify_use_case_task:
  description: >
    Analyze the user input, metadata, and conversation history to determine which of the following use cases it falls under:

    1) General question:  
    The user is asking about the structure, contents, or possibilities offered by the data.  
    In this case, use_case_id should be set to 'general' and a clear restatement of the user intent included.

    2) Data question:  
    The user is asking for specific information that requires querying one or more tables.  
    In this case, use_case_id should be set to 'data' and the user intent must be restated clearly along with all necessary query-related details (e.g., filters, joins, aggregations) based only on metadata.

    3) Scenario question:  
    The user is asking a hypothetical or “what if” question involving changes to organizational structure, headcount, or resource allocation.  
    In this case, use_case_id should be set to 'scenario' and each change should be captured precisely along with a restated user intent.

    4) Clarification question:  
    The user input is ambiguous or lacks sufficient information to classify.  
    In this case, use_case_id should be set to 'clarification' and a clear follow-up question should be provided to request the missing information.

    You MUST classify the user input into one of these use cases.

    If you are unable to determine the correct use case with certainty, respond with a clarification question addressed directly to the user.

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
