MATCH (r:Role)-[:FILLED_BY]->(res:Resource),
      (cr:CanonicalRole)-[:CANONICAL_FOR]->(r)
RETURN cr.name AS canonical_role, COUNT(DISTINCT res) AS resource_count
ORDER BY resource_count DESC
