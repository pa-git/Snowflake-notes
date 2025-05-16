<TIP>
If a Cypher query returns no results, consider common issues:

1. **Exact string match** – Neo4j is case-sensitive. Double-check names, especially for labels or node properties like `division`, `vendor`, or `role`.

2. **Relationship structure** – Queries often fail when multiple relationships are incorrectly chained. For example, a contract may link separately to a division and a vendor, not through a path. Use separate `MATCH` clauses when needed.

3. **Missing joint relationships** – The node you're querying may exist, but not in combination. Always confirm that the same contract connects to both nodes involved.
</TIP>
