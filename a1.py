<INSTRUCTIONS>
Analyze the input text and the previously extracted services to identify all roles associated with each service. 
For every service, include its corresponding service number and list all related roles.

For each role, extract the following fields:

- Role number: Assign based on order of appearance (e.g., 1, 2, 3...). Add clarification in parentheses if needed.
- Role name: The name or title of the role.
- Number of resources: Specify the number of individuals assigned to this role (default to 1 if not specified).
- Resource names: List names of assigned individuals, if available (separate multiple names by commas).
- Role description: A clear summary of the work to be performed.
- Skill or seniority level: Capture any mention of experience, level, or qualification.
- Role location: The location where the role is based or performed.
- Rate amount: A numeric value representing the rate for this role.
- Rate period: MUST be one of the following — Hourly, Daily, Monthly, or Annually.
- Currency: The currency in which the rate is provided.
- Rate commitment: The quantity of hours, days, months, etc. for which the role is committed.
- Total fees: The calculated total for this role (e.g., if the rate is 100, period is Daily, and commitment is 30, then total = 100 * 30 = 3000).

</INSTRUCTIONS>
