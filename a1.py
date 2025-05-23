Here’s the updated agent prompt instructions with both required clarifications:

---

> 1. When using `GROUP BY` in Cypher, always use a `WITH` clause first to perform the grouping, and then use `RETURN` to output the grouped results. For example:
>
> ```cypher
> MATCH (r:Role)-[:IS_CANONICAL_ROLE]->(cr:CanonicalRole {name: "Resource and Personnel Management"})
> WITH r.location AS country, r.city AS city, r.level AS level, r.rate_currency AS currency, AVG(r.rate_amount) AS average_rate
> RETURN country, city, level, currency, average_rate
> ```
>
> 2. When grouping or aggregating by location (e.g., for counts, averages, etc.), **always use the canonical location** node (e.g., `(r)-[:IS_IN_LOCATION]->(:CanonicalLocation)`) to ensure consistent regional analysis.
