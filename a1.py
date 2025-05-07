---

For the user input:  
`"What are the contracts for the Finance division?"`

Expected response format:
```json
{
  "analysis_plan": "Identify all contracts associated with the Finance division. Use the 'division' filter to limit results to that division, and the 'section' filter to retrieve only Contract Metadata. Return a list of contracts that belong to the Finance division with their key metadata details.",
  "query": "",
  "filters": {
    "source": null,
    "vendor": null,
    "division": "Finance",
    "section": "Contract Metadata"
  }
}
