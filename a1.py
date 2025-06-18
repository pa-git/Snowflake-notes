<INSTRUCTIONS>

Analyze the input text to determine whether the contract includes any resource groups or individuals that qualify as non-conforming based on their billing or staffing status.

Non-conforming resources are typically used for internal cost tracking, not tied to direct delivery, and are often referred to using the following terms: bench, free, non-billable, idle, or cost-center only.

If any non-conforming resources are found, extract the following fields:

- resource_description: A short description or name identifying the resource group or role (e.g., "QA bench", "non-billable developers").
- non_conformity_type: Must be one of the following — non-billable, bench, or free.

If no non-conforming resources are found, return:
{ "non_conforming_resources": [] }

</INSTRUCTIONS>
