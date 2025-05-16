MATCH (c:Contract)-[:IS_FOR_DIVISION]->(d:CanonicalDivision {name: 'Cyber Data Risk & Resilience'})
WITH replace(c.total_fee, ",", "") AS fee
RETURN SUM(toFloat(fee)) AS total_spending
