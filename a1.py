<CONVERSATION_HISTORY>
{conversation_history}
</CONVERSATION_HISTORY>

<LATEST_USER_INPUT>
{user_input}
</LATEST_USER_INPUT>

<INSTRUCTIONS>
Analyze the conversation history and the latest user input to create a clear plan for addressing the query. Your response must include:

1) **Analysis Plan**:
- Outline the steps to answer the user's question, specify the information to retrieve, and explain how to use it to provide the best response.

2) **Search Query**:
- Provide the search term for a semantic search against the contracts data. Leave empty if retrieving an entire section, such as all "Roles" in all contracts.

3) **Filters**:
- Specify filters for the search to retrieve relevant information. Available filters include:
  - **source**: Contract document name (e.g., "Unified Managed Services Contract v5"). Use for specific contracts.
  - **vendor**: Vendor name (e.g., "Ernst & Young LLP"). Use for specific vendors.
  - **division**: Division name (e.g., "Finance"). Use for specific divisions.
  - **section**: Contract section (e.g., "Roles"). Select only one of the following:
    - Contract Metadata: Basic contract details (name, type, dates, parties).
    - Financials: Fees, payments, exclusions, and terms.
    - Services: Service details, quantities, prices, and notes.
    - Service Level Agreements: Performance targets, penalties, mechanisms.
    - Roles: Project roles, personnel, hours, rates, billing.
    - Scope and Structure: Project details, timelines, divisions, initiatives.
    - Applications and Expectations: Supported applications, key activities, assumptions.
</INSTRUCTIONS>

<EXAMPLES>

<EXAMPLE>
<USER_INPUT>What are the most common services?</USER_INPUT>
<EXPECTED_OUTPUT>
{
  "analysis_plan": "Retrieve all services from all available contracts. Normalize service descriptions to group similar services (e.g., 'Application Testing', 'Software QA'). Count how many times each normalized service appears. Return an ordered list of the most common services ranked by frequency.",
  "query": "",
  "source": "",
  "vendor": "",
  "division": "",
  "section": "Services"
}
</EXPECTED_OUTPUT>
</EXAMPLE>

<EXAMPLE>
<USER_INPUT>What are the vendors that provide QA services?</USER_INPUT>
<EXPECTED_OUTPUT>
{
  "analysis_plan": "Search all available contracts for roles related to QA. Identify the vendors associated with those roles. Normalize QA role titles (e.g., 'QA Analyst', 'Test Engineer'). For each vendor, extract the rates or rate ranges of QA roles they provide. Return a deduplicated list of vendors along with their corresponding QA rate or rate range.",
  "query": "Quality Assurance",
  "source": "",
  "vendor": "",
  "division": "",
  "section": "Roles"
}
</EXPECTED_OUTPUT>
</EXAMPLE>

<EXAMPLE>
<USER_INPUT>Create a grid of similar roles comparing it by vendors and average rate for all the vendors</USER_INPUT>
<EXPECTED_OUTPUT>
{
  "analysis_plan": "Retrieve all roles from all contracts. Normalize titles to group similar roles across vendors (e.g., 'Software Engineer', 'Developer', 'Programmer'). For each normalized role, calculate the average rate per vendor. Construct a grid where rows represent the normalized roles and columns represent vendors, with each cell showing the average rate for that role by that vendor.",
  "query": "",
  "source": "",
  "vendor": "",
  "division": "",
  "section": "Roles"
}
</EXPECTED_OUTPUT>
</EXAMPLE>

<EXAMPLE>
<USER_INPUT>What are the contracts for the Finance division?</USER_INPUT>
<EXPECTED_OUTPUT>
{
  "analysis_plan": "Retrieve all contracts associated with the Finance division. Use the 'division' filter to limit results to that division, and the 'section' filter to retrieve only Contract Metadata. Return a list of contracts that belong to the Finance division with their key metadata details.",
  "query": "",
  "source": "",
  "vendor": "",
  "division": "Finance",
  "section": "Contract Metadata"
}
</EXPECTED_OUTPUT>
</EXAMPLE>

</EXAMPLES>
