extract_contract_overview:
  description: >
    Analyze the text received in order to extract all relevant details required to populate the ContractOverviewModel output JSON object.

    **Important**:
    - You MUST not invent any information that is not explicitly provided in the text received.
    - Include any fee or invoicing schedule under `financials`.
    - Include contract file name, type, summary, and dates under `contract_metadata`.
    - Include all signature details under `signatures`.

    Inputs:
    - Text received from the previous task
    - File name delimited by triple backticks: ```{file_name}```

  expected_output: ContractOverviewModel
  agent: ocr_text_analyzer
  output_file: output/ocr_json/{file_name}/overview.json
  context:
    - review_ocr_text

extract_services_and_roles:
  description: >
    Analyze the text received in order to extract all relevant details to populate the ServicesAndRolesModel output JSON object.

    **Important**:
    - You MUST not invent any information that is not explicitly provided.
    - Under `services`, extract descriptions, coverage, pricing, and periods.
       - Under `roles`, include every available field such as `role_name`, `resource_name`, `description`, `location`, `level`, `hours_committed`, `rate`, `billing_type`, `schedule_reference`, `total_fees`, and `project`.


    Inputs:
    - Text received from the previous task
    - File name delimited by triple backticks: ```{file_name}```

  expected_output: ServicesAndRolesModel
  agent: ocr_text_analyzer
  output_file: output/ocr_json/{file_name}/services_roles.json
  context:
    - review_ocr_text

extract_governance_and_scope:
  description: >
    Analyze the text received to extract all data relevant to service level agreements, governance meetings/reports, and engagement scope. This should populate the GovernanceAndScopeModel output JSON object.

    **Important**:
    - Do not invent any targets or frequencies.
    - Include all listed SLAs with enforcement methods and applicable services.
    - Extract assumptions, conditions, and client/vendor expectations from the engagement scope.

    Inputs:
    - Text received from the previous task
    - File name delimited by triple backticks: ```{file_name}```

  expected_output: GovernanceAndScopeModel
  agent: ocr_text_analyzer
  output_file: output/ocr_json/{file_name}/governance_scope.json
  context:
    - review_ocr_text

extract_contextual_info:
  description: >
    Analyze the text received and extract information on divisions, initiatives, projects, deliverables, and involved parties. Use this to populate the ContextualModel output JSON object.

    **Important**:
    - Use only explicitly listed projects, with associated dates, status, and descriptions.
    - Include all parties mentioned, their roles, addresses, and contextual notes.
    - Include each deliverable and invoice amount with relevant dates and percentages.

    Inputs:
    - Text received from the previous task
    - File name delimited by triple backticks: ```{file_name}```

  expected_output: ContextualModel
  agent: ocr_text_analyzer
  output_file: output/ocr_json/{file_name}/context.json
  context:
    - review_ocr_text
