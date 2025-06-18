<INSTRUCTIONS>
Analyze the input text to identify whether any acceptance criteria are explicitly defined in the contract.

Acceptance criteria refer to the specific conditions, deliverables, performance levels, or review processes that must be met for the client to formally approve the work. These may include references to quality checks, sign-off steps, milestone completion, performance thresholds, review protocols, or any requirements tied to payment or project closure.

Extract the following fields:

- acceptance_criteria_present: Return `true` if the contract defines one or more acceptance criteria. Return `false` if no such criteria are mentioned.

- acceptance_criteria: If acceptance criteria are present, list each one as a standalone string using the exact or paraphrased language from the contract. If none are present, return an empty list.

Return a single JSON object with both fields.
</INSTRUCTIONS>
