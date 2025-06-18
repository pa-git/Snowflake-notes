<INSTRUCTIONS>
Analyze the input text to extract all relevant information related to the governance structure and delivery methodology of the contract.

You must extract the following four fields:

- methodology_keywords: Capture the exact text from the contract that describes the delivery methodology used for the work. This includes references to Agile, Waterfall, ITIL, DevOps, or any other structured method or framework. If multiple methodologies are mentioned, include all of them in the string.

- milestone_defined: Indicate whether the contract explicitly defines any milestones for deliverables, project phases, or completion checkpoints. Return "yes" if any formal milestones or phases are described; otherwise, return "no".

- acceptance_criteria_defined: Indicate whether the contract includes specific acceptance criteria for deliverables. This refers to formal conditions under which a deliverable is accepted, such as functional completeness, client sign-off, test results, or review procedures. Return "yes" if acceptance terms are clearly stated; otherwise, return "no".

- team_management_structure: Identify who is responsible for managing the delivery team during the execution of the contract. Return one of the following values based on the text:
  - "vendor-led": if the vendor is clearly described as managing the delivery team
  - "client-led": if the client or internal team is responsible for oversight
  - "shared": if responsibility is described as joint or collaborative
  - "not specified": if the contract does not clearly assign management responsibility

Return only the extracted values in a valid JSON object using the specified field names.
</INSTRUCTIONS>
