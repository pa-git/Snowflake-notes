<TIPS>
- Avoid chaining multiple relationships in a single path unless you're certain the connections exist as such. Use separate MATCH clauses when needed.

- Always use relationships exactly as defined in the SCHEMA under <RELATIONSHIPS>. Do not invent or assume relationships that aren’t explicitly listed.

- When identifying the most common roles or services, use CanonicalRole and CanonicalService nodes to ensure normalized comparisons.

- When working with rates, always convert values to USD before aggregating or comparing across contracts.

- If a user refers to a vendor using an acronym or shorthand, resolve it to the vendor’s full company name before querying.

- When returning tables that include counts, totals, or amounts, sort the results in descending order to highlight the most significant values first.

- If a query returns no results, double-check for:
  • Case-sensitive or misspelled property values (e.g., division names)  
  • Incorrectly chained relationships that should be modeled separately  
  • Missing joint links—ensure the same node (e.g., a Contract) connects to all queried entities
</TIPS>
