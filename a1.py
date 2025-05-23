Here’s the revised prompt instruction, updated to reflect that **`GROUP BY` cannot be used** and that **`WITH` must be used for aggregation instead**:

---

> 1. Do **not** use `GROUP BY` in Cypher. Instead, use a `WITH` clause to perform aggregations like `AVG`, `COUNT`, etc. For example:
>
> ```cypher
> MATCH (r:Role)-[:IS_CANONICAL_ROLE]->(cr:CanonicalRole {name: "Resource and Personnel Management"})
> WITH r.location AS country, r.city AS city, r.level AS level, r.rate_currency AS currency, AVG(r.rate_amount) AS average_rate
> RETURN country, city, level, currency, average_rate
> ```
>
> 2. When grouping or aggregating by location, always use the **canonical location node** (e.g., via `(r)-[:IS_IN_LOCATION]->(cl:CanonicalLocation)`), not raw or unnormalized fields, to ensure consistency.
