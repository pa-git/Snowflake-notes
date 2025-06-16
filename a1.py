<INSTRUCTIONS>
Use the input text and the list of extracted services provided in the context to identify all roles associated with each service. 
For every service, include its corresponding service number and list all roles related to that service.

For each role, extract the following fields:

- Role number: Assign based on the order of appearance (e.g., 1, 2, 3...). Add clarification in parentheses if needed.
- Role name: The name or title of the role.
- Number of resources: Specify the number of individuals assigned to this role (default to 1 if not explicitly stated).
- Resource names: List the names of assigned individuals, if provided (separate multiple names with commas).
- Role description: A clear summary of the work this role performs.
- Skill or seniority level: Capture any mention of experience level, qualification, or skill tier.
- Role location: The location where the role is to be performed.
- Rate amount: A numeric value indicating the cost per rate period.
- Rate period: MUST be one of the following — Hourly, Daily, Monthly, or Annually.
- Currency: The currency in which the rate is specified.
- Rate commitment: The number of hours, days, or months this role is committed for.
- Total fees: Calculate the total fees for the role. For example, if the rate is 100, the period is Daily, and the commitment is 30, then total = 100 × 30 = 3000.

</INSTRUCTIONS>
