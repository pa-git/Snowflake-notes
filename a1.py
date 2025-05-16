MATCH (c:Contract)-[:IS_FOR_DIVISION]->(d:CanonicalDivision {name: 'Cyber Data Risk & Resilience'})
MATCH (c)-[:IS_WITH_VENDOR]->(v:CanonicalVendor)
RETURN DISTINCT v.name AS VendorName
