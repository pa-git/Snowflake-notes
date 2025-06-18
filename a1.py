<INSTRUCTIONS>
Analyze the input text to extract all relevant information related to the tools and platforms mentioned in the delivery of the service.

You must extract two distinct lists: one for tool types and one for platform scope. Use only the allowed values provided for each field. If a concept is mentioned that does not match any allowed value but is clearly relevant, include it as "other".

Extract the following fields:

- tool_types_mentioned: List all tool categories explicitly mentioned in the text that are used to support the delivery of the service. This includes technical tools, software, or systems used for activities such as automation, deployment, data handling, or reporting. Examples include CI/CD, test automation, and BI tools.

  Allowed values:
  - test automation
  - CI/CD
  - data pipeline tools
  - ETL tools
  - business intelligence tools
  - APIs
  - source control tools
  - performance monitoring tools
  - cloud infrastructure tools
  - project management tools
  - other

- platform_scope: List all platforms referenced in the contract as being within the scope of the work. This refers to the types of technology environments or system layers involved in delivering the service.

  Allowed values:
  - web
  - mobile
  - embedded
  - mainframe
  - cloud
  - on-premise
  - distributed systems
  - other

Return a single JSON object with both fields, strictly using the allowed values.
</INSTRUCTIONS>
