Here’s the updated prompt instruction with the example query modified to use the **canonical location**:

---

> 1. Do **not** use `GROUP BY` in Cypher. Instead, use a `WITH` clause to perform aggregations like `AVG`, `COUNT`, etc. For example:
>
> ```cypher
> MATCH (r:Role)-[:IS_CANONICAL_ROLE]->(cr:CanonicalRole {name: "Resource and Personnel Management"})
> MATCH (r)-[:IS_IN_LOCATION]->(cl:CanonicalLocation)
> WITH cl.country AS country, cl.city AS city, r.level AS level, r.rate_currency AS currency, AVG(r.rate_amount) AS average_rate
> RETURN country, city, level, currency, average_rate
> ```
>
> 2. When grouping or aggregating by location, always use the **canonical location node** (e.g., `CanonicalLocation`) to ensure consistent and normalized geographic data.
