<INSTRUCTIONS>
Analyze the input text to extract all relevant information related to the business context and purpose of the contracted service.

You must extract the following two fields:

- primary_goal: Identify the main business purpose of the service as stated or implied in the contract. This may include objectives such as strategic guidance, system modernization, long-term operational support, technical upgrades, or compliance initiatives. Use the following categories and select the one that most accurately represents the intent of the engagement:
  • advisory  
  • modernization  
  • operational continuity  
  • upgrade  
  • compliance  
  • strategic planning  
  • technical delivery  
  • support

- business_area: Identify the business or technical domain where the service is being applied, based on the type of work, technologies referenced, or business function described. This reflects the scope or environment in which the service will operate. Choose the most appropriate label from the following:
  • infrastructure  
  • application development  
  • data and analytics  
  • compliance and risk  
  • automation  
  • IT operations  
  • enterprise architecture  
  • cloud and platform engineering

You must assign exactly one value for each field. If the input text references more than one candidate, select the one most emphasized or most relevant to the primary work being contracted.

Return only valid JSON using the specified field names.

</INSTRUCTIONS>
