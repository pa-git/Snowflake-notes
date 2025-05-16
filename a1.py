MATCH (r:Role)-[:IS_CANONICAL_ROLE]->(cr:CanonicalRole)
MATCH (c:Contract)-[:INCLUDES_ROLE]->(r)
MATCH (c)-[:IS_FOR_DIVISION]->(d:CanonicalDivision)
WHERE cr.name CONTAINS 'Software'
RETURN cr.name, d.name, COUNT(r)
