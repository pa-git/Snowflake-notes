MATCH (p:Person)-[:HAS_ROLE]->(r:Role)-[:IS_A]->(cr:CanonicalRole)
RETURN cr.name AS role, count(DISTINCT p) AS people_count
ORDER BY people_count DESC
