<INSTRUCTIONS>
Analyze the input text to extract all relevant information related to the commercial and engagement structure of the consulting service.

Extract the following fields with precision:

- engagement_model: Identify the overall commercial model used for the contract. Choose one of the following:
  - "fixed-price": The vendor is paid a fixed amount for a defined scope of work, regardless of time or resources used.
  - "time-and-materials": The vendor is paid based on the actual time spent and materials used.
  - "managed service": The vendor delivers predefined services on a recurring basis, usually under SLAs, and is responsible for outcomes.
  - "staff augmentation": The vendor supplies personnel to work under the client's direction, typically without ownership of deliverables.

- billing_basis: Determine how the vendor is compensated for the work. Choose one of the following:
  - "milestone-based": Payment is tied to the completion of specific milestones or deliverables.
  - "monthly retainer": The vendor is paid a fixed recurring fee (usually monthly) for ongoing services.
  - "hourly": The vendor is paid based on the number of hours worked.
  - "deliverable-based": Payment is tied to the submission or approval of defined deliverables.

- duration_model: Identify the duration structure of the engagement. Choose one of the following:
  - "ongoing": The contract supports continuous services with no fixed end date.
  - "long-term": The contract spans a significant, predefined duration (e.g., one year or more).
  - "project-based": The contract is tied to a specific project with a defined scope and timeline.
  - "ad hoc": The work is requested and delivered on an as-needed, sporadic basis.

You must infer each value based on the language used in the contract, such as descriptions of payment terms, engagement type, or delivery expectations. Return only the values listed above for each field.
</INSTRUCTIONS>
