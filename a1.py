<INSTRUCTIONS>
Analyze the input text to extract relevant information about the delivery methodology and governance structure for the contracted work.

Extract the following fields:

- methodology_keywords: List any delivery or governance methodologies explicitly mentioned in the contract. These include named approaches like Agile, Scrum, ITIL, or DevOps. If no methodology is mentioned, return ["none"]. If an unlisted methodology is mentioned, include "other".

  Allowed values:
  - Agile
  - Scrum
  - Kanban
  - Waterfall
  - ITIL
  - DevOps
  - none
  - other

- team_management_structure: Identify who is responsible for managing the team and overseeing the execution of the work. Choose from:
  - "vendor-led" — if the vendor manages the delivery
  - "client-led" — if the client directly manages the team
  - "shared" — if management responsibility is explicitly shared
  - "unclear" — if not enough information is available

Return a single JSON object with both fields.
</INSTRUCTIONS>
