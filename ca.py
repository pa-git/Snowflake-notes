---
**Example Output:**

---

For the user input:  
`"What are the most common services?"`

Expected response format:
{
  "analysis_plan": "Retrieve all services from all available contracts. Normalize service descriptions to group similar services (e.g., 'Application Testing', 'Software QA'). Count how many times each normalized service appears. Return an ordered list of the most common services ranked by frequency.",
  "query": "",
  "filters": {
    "source": null,
    "vendor": null,
    "section": "Services"
  }
}

---

For the user input:  
`"What are the vendors that provide QA services?"`

Expected response format:
{
  "analysis_plan": "Search all available contracts for roles related to QA. Identify the vendors associated with those roles. Normalize QA role titles (e.g., 'QA Analyst', 'Test Engineer'). For each vendor, extract the rates or rate ranges of QA roles they provide. Return a deduplicated list of vendors along with their corresponding QA rate or rate range.",
  "query": "QA roles or quality assurance personnel",
  "filters": {
    "source": null,
    "vendor": null,
    "section": "Roles"
  }
}

---

For the user input:  
`"Create a grid of similar roles comparing it by vendors and average rate for all the vendors"`

Expected response format:
{
  "analysis_plan": "Retrieve all roles from all contracts. Normalize titles to group similar roles across vendors (e.g., 'Software Engineer', 'Developer', 'Programmer'). For each normalized role, calculate the average rate per vendor. Construct a grid where rows represent the normalized roles and columns represent vendors, with each cell showing the average rate for that role by that vendor.",
  "query": "",
  "filters": {
    "source": null,
    "vendor": null,
    "section": "Roles"
  }
}
