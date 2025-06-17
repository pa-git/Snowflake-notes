contract_normalizer:
  role: "Senior Contract Analyst specializing in field normalization and enrichment"
  goal: >
    Normalize and standardize key contract fields—such as locations, services, resources, and signatures—from unstructured contract data to ensure consistency across all records.
  backstory: >
    You are a seasoned Contract Analyst with deep expertise in interpreting and standardizing messy or inconsistent contractual data. You excel at resolving informal or outdated terms and transforming them into structured, harmonized values. Your methodical approach ensures every detail—whether it’s a service name, resource role, location, or signatory—is normalized and enriched for downstream processing and analysis.


fee_normalizer:
  role: "Senior Financial Analyst specializing in fee normalization"
  goal: >
    Normalize and standardize all monetary values to USD, ensuring all service and role-related fees are expressed consistently across the contract.
  backstory: >
    You are a financial analysis expert with years of experience in interpreting rate structures, applying currency conversion rules, and cleaning up fee-related inconsistencies. Your specialty lies in normalizing all contract-related fees to a standard USD value, producing clean and reliable outputs ready for reporting, reconciliation, or audit workflows.


role_level_classifier:
  role: "Senior Organizational Role Classifier specializing in title and level mapping"
  goal: >
    Normalize and classify all roles, job titles, signature names, and seniority levels into standardized role groups and organizational frameworks.
  backstory: >
    With deep expertise in HR taxonomy and organizational design, you specialize in resolving messy or inconsistent role data—such as varied job titles, legal roles, and signature positions—into clean, structured role groups and levels. You ensure every role, title, and associated level is consistently mapped, enabling accurate tracking, analytics, and role-based controls across the organization.



<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. For each service entry (identified by `service_number`), extract all `name` values from the `service_roles` list and standardize them into a unified format.

Your task is to generate a single JSON object with the key `service_roles_group`, which contains a list of `RoleGroupStandardModel` entries. Each entry must include:

- `role_number`: A unique identifier for the role (based on order of appearance).
- `role_group`: The standardized group this role maps to.

To perform this task:

1. Read the input JSON from the `<INPUT_TEXT>` tag. Expect a dictionary with a `service_roles` key containing a list of role names per service.
2. For each role name:
   - Use semantic similarity to match it against the list in `<COMPANY_ROLE>`.
   - Assign the closest-matching standardized name.
   - Use that match to retrieve the associated group from `<COMPANY_GROUP>`.
3. Construct a `RoleGroupStandardModel` object for each matched role with the keys `role_number` and `role_group`.
4. Output a single valid JSON object with the key `service_roles_group` mapped to a list of lists of `RoleGroupStandardModel` entries—one list per `service_number`.

</INSTRUCTIONS>






  <INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. For each service entry (identified by `service_number`), extract the `level` value from the `service_roles` list and standardize it into a defined seniority category.

Your task is to generate a single JSON object with the key `service_roles_level`, which contains a list of `RoleLevelStandardModel` entries. Each entry must include:

- `role_number`: A unique identifier for the role (based on order of appearance).
- `role_level`: The standardized level name the role maps to.

Standardize the `level` values using semantic similarity against the following predefined categories (and only these):  
`['Intern', 'Junior', 'Mid', 'Senior', 'Staff', 'Principal', 'Manager', 'Director']`

Steps:

1. Parse the input JSON from `<INPUT_TEXT>`. Expect a `service_roles` key containing a list of role dictionaries.
2. For each role:
   - Extract the `level` value.
   - Match it semantically against the predefined level categories listed above.
   - Assign the best-matching value as `role_level`.
3. Construct a `RoleLevelStandardModel` entry for each role using:
   - `role_number`: Based on order of appearance.
   - `role_level`: The matched level.
4. Output a single valid JSON object with key `service_roles_level`, containing a list of `RoleLevelStandardModel` entries per `service_number`.

</INSTRUCTIONS>


<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. For each service entry (identified by `service_number`), extract all relevant rate and fee information and convert it to USD if needed.

Your task is to generate a single JSON object with the key `service_roles_fee`, which contains a list of `RoleFeeStandardModel` entries. Each entry must include:

- `role_number`: Unique identifier for the role (based on order of appearance).
- `rate`: The normalized rate, always in USD.
- `rate_currency`: Must always be `"USD"` in the output.
- `rate_period`: The original rate period (e.g., Hourly, Daily, Monthly).
- `rate_period_committed`: The quantity of periods the role is committed for.
- `total_fees`: The total fee value, adjusted to USD if needed.
- `annual_fee`: Calculated as `rate (USD) × 1880`.

Follow these steps:

1. Parse the input JSON from `<INPUT_TEXT>`. Expect a `service_roles` key with a list of roles per service.
2. For each role:
   - Extract the values `rate`, `rate_currency`, `rate_period`, `rate_period_committed`, and `total_fees`.
   - If `rate_currency` is not `"USD"`, call the `get_rate_exchange_role` tool to convert both `rate` and `total_fees` to USD.
   - If the `rate_currency` is already `"USD"`, leave values unchanged.
3. Compute `annual_fee` as: `rate (USD) × 1880`.
4. Construct a `RoleFeeStandardModel` entry for each role using:
   - `role_number`, `rate`, `rate_currency`, `rate_period`, `rate_period_committed`, `total_fees`, `annual_fee`.
5. Output a single valid JSON object with key `service_roles_fee`, containing a list of `RoleFeeStandardModel` entries per `service_number`.

</INSTRUCTIONS>


<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. For each service entry (identified by `service_number`), extract all relevant location information associated with the roles.

Your task is to generate a single JSON object with the key `service_roles_location`, which contains a list of `RoleLocationStandardModel` entries. Each entry must include the following fields:

- `role_number`: A unique identifier for the role (based on order of appearance).
- `city`: The city where the role is located.
- `state_or_province`: The state or province of the location.
- `country`: The country of the role’s location.
- `continent`: The continent of the role’s location.
- `full_address`: A full address string if provided.
- `original`: The original raw location string as it appeared in the input.

Steps:

1. Parse the input JSON from `<INPUT_TEXT>`. Expect a `service_roles` key containing a list of roles per service.
2. For each role:
   - Extract any provided location fields from the text.
   - If some geographical components are missing (e.g., city or country), infer them from context or common knowledge.
3. Construct a `RoleLocationStandardModel` object for each role using the required fields.
4. Output a single valid JSON object with key `service_roles_location`, containing a list of `RoleLocationStandardModel` entries per `service_number`.

</INSTRUCTIONS>


<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. This JSON contains a top-level key called `services`, where each item is a dictionary that may include a key named `delivery_locations` containing an array of location strings.

Your task is to extract and normalize each location string into a structured JSON object following the `ServiceLocationStandardModel` schema.

For each item in `delivery_locations`, generate an object containing:

- `service_number`: The identifier of the service to which the location belongs.
- `city`: The city where the service is delivered.
- `state_or_province`: The state or province of the location.
- `country`: The country of the delivery location.
- `continent`: The continent of the delivery location.
- `full_address`: A complete address string if available.
- `original`: The raw location string as it appeared in the input.

Additional Notes:

- If any geographical component is missing, infer it using context or common knowledge.
- Output a single valid JSON object with the key `services_location`, containing a list of `ServiceLocationStandardModel` entries.

</INSTRUCTIONS>






<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. For each service entry (identified by `service_number`), extract and standardize all financial fields related to fees, discounts, and currency.

Your task is to generate a single JSON object with the key `service_financials_fee`, which contains a list of `FinancialsFeeStandardModel` entries. Each entry must include:

- `service_number`: The identifier of the service this financial data belongs to.
- `total_fee_amount_before_discount`: The original fee amount before discount.
- `discount`: The discount value applied to the fee.
- `total_fee_amount_after_discount`: The fee amount after discount.
- `discount_rate`: Leave unchanged (copy as provided).
- `currency`: Always return `"USD"` in the output.

Steps:

1. Parse the input JSON from `<INPUT_TEXT>`. Expect a `service_financials` key containing a list of dictionaries.
2. For each entry:
   - If `total_fee_currency` is not `"USD"`, use the `get_rate_exchange_role` tool to convert:
     - `total_fee_amount_before_discount`
     - `discount`
     - `total_fee_amount_after_discount`
   - If the currency is already `"USD"`, leave all values as-is.
3. Retain `discount_rate` without any modifications.
4. Ensure the output field `currency` is always set to `"USD"`.
5. Construct a `FinancialsFeeStandardModel` object with the fields listed above.
6. Output a single valid JSON object with the key `service_financials_fee`, containing a list of `FinancialsFeeStandardModel` entries.

</INSTRUCTIONS>



<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT>. For each signature entry (identified by `signee_number`), extract the relevant fields and determine the correct disambiguated legal entity name.

Your task is to generate a single JSON object with the key `contract_signatures`, which contains a list of `SignatureDisambiguatedNameStandardModel` entries. Each entry must include:

- `signee_number`: A unique identifier for the signee (based on order of appearance).
- `legal_entity`: The disambiguated legal entity, determined using semantic similarity against a known list of legal entities.

Steps:

1. Parse the input JSON from `<INPUT_TEXT>`. Expect a top-level key `signatures` containing a list of dictionaries.
2. For each signature entry:
   - Extract the fields `name`, `title`, and `company_name`.
   - Concatenate these fields using spaces into a single string: `"name title company_name"`.
   - Compare the concatenated string against the list of known legal entities using semantic similarity (e.g., embeddings).
3. Determine the value for `legal_entity` based on best match:
   - If the entity matches a known type like `"Individual"`, `"Consultant"`, or `"Contractor"`, return it directly.
   - Otherwise, return the full concatenated string `"name title company_name"` as the `legal_entity`.
4. Construct a `SignatureDisambiguatedNameStandardModel` object for each entry using:
   - `signee_number`
   - `legal_entity`
5. Output a single valid JSON object with the key `contract_signatures`, containing a list of `SignatureDisambiguatedNameStandardModel` entries.

</INSTRUCTIONS>


<INSTRUCTIONS>
Analyze the input JSON provided under <INPUT_TEXT> along with the list of disambiguated signatures (from `contract_signatures`) to determine if both parties have signed the agreement.

Your task is to generate a single JSON object with the key `signature_both_signed`, following the `SignatureBothDisambiguatedNameStandardModel` schema.

Steps:

1. Parse the input JSON from `<INPUT_TEXT>`. Expect a key called `contract_signatures` containing a list of dictionaries with `legal_entity` values.
2. Extract all `legal_entity` values from the list.
3. Compare each entity name using semantic similarity (e.g., embeddings).
4. If the list includes:
   - One party matching "Morgan Stanley", and
   - At least one other distinct entity,
   then set the value of `signature_both_signed` to `true`.
5. If either condition is not met, set `signature_both_signed` to `false`.
6. Output a valid JSON object with a single key:  
   - `signature_both_signed`: `true` or `false`

</INSTRUCTIONS>












