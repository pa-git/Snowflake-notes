<INSTRUCTIONS>

Analyze the input text to identify and extract all Travel and Expense (T&E) details mentioned in the contract.

For each T&E clause or section, extract the following fields:

- description: A clear explanation of the travel and expense policy or terms as stated in the contract.
- fee_type: Classify the T&E as one of the following — reimbursable, non-reimbursable, or pass-through.
- cap_amount: If a maximum reimbursable or allowable amount is specified, extract it as a numeric value.
- currency: The currency in which the cap amount or T&E costs are stated (e.g., USD, EUR).
- billing_method: The method used to calculate or charge T&E costs. Must be one of: actuals, per diem, or estimated.
- approval_required: Indicate whether prior approval is explicitly required for the T&E to be reimbursed (true or false).

If no T&E-related content is present, return an empty array.

</INSTRUCTIONS>
