-- 1. Most common roles --
MATCH (r:Role)
RETURN r.name AS role, COUNT(*) AS count
ORDER BY count DESC

-- 2. Average rate for the role of Manager --
MATCH (r:Role {name: "Manager"})
RETURN AVG(r.rate_amount) AS avg_rate

-- 3. Rate by vendor for the role of Developer --
MATCH (r:Role {name: "Developer"})<-[:INCLUDES_ROLE]-(c:Contract)-[:SIGNED_BY_VENDOR]->(v:Party)
RETURN v.name AS vendor, AVG(r.rate_amount) AS avg_rate
ORDER BY avg_rate DESC

-- 4. Do we have any contracts for QA --
MATCH (c:Contract)-[:INCLUDES_SERVICE]->(s:Service)
WHERE TOLOWER(s.name) CONTAINS "qa"
RETURN DISTINCT c.file_name AS contract, s.name AS service

-- 5. Grid of similar roles by vendors and avg rate --
MATCH (r:Role)<-[:INCLUDES_ROLE]-(c:Contract)-[:SIGNED_BY_VENDOR]->(v:Party)
RETURN r.name AS role, v.name AS vendor, AVG(r.rate_amount) AS avg_rate
ORDER BY role, vendor

-- 6. Vendors that provide QA services --
MATCH (c:Contract)-[:INCLUDES_SERVICE]->(s:Service), (c)-[:SIGNED_BY_VENDOR]->(v:Party)
WHERE TOLOWER(s.name) CONTAINS "qa"
RETURN DISTINCT v.name AS vendor

-- 7. Consultants with their start date --
MATCH (r:Role)
WHERE TOLOWER(r.name) CONTAINS "consultant"
WITH r
MATCH (r)<-[:INCLUDES_ROLE]-(c:Contract)
RETURN DISTINCT r.resource_name AS consultant, c.start_date AS contract_start
ORDER BY consultant

-- 8. All contracts for EY --
MATCH (c:Contract)-[:SIGNED_BY_VENDOR]->(v:Party)
WHERE TOLOWER(v.name) CONTAINS "ey"
RETURN c.file_name AS contract, c.start_date, c.end_date

-- 9. Total payments to EY --
MATCH (c:Contract)-[:SIGNED_BY_VENDOR]->(v:Party)
WHERE TOLOWER(v.name) CONTAINS "ey"
RETURN v.name AS vendor, SUM(TOFLOAT(REPLACE(REPLACE(c.total_fee, '$', ''), ',', ''))) AS total_paid

-- 10. Contracts by division --
MATCH (c:Contract)
RETURN c.division AS division, COUNT(*) AS count
ORDER BY count DESC

-- 11. Vendors working with Internal Audit Division --
MATCH (c:Contract {division: "Internal Audit"})-[:SIGNED_BY_VENDOR]->(v:Party)
RETURN DISTINCT v.name AS vendor

-- 12. Contracts per vendor --
MATCH (c:Contract)-[:SIGNED_BY_VENDOR]->(v:Party)
RETURN v.name AS vendor, COUNT(*) AS contracts
ORDER BY contracts DESC

-- 13. Resources per role --
MATCH (r:Role)-[:ASSIGNED_TO]->(p:CanonicalPerson)
RETURN r.name AS role, COUNT(p) AS resource_count
ORDER BY resource_count DESC

-- 14. Developer rate statistics by vendor --
MATCH (r:Role {name: "Developer"})<-[:INCLUDES_ROLE]-(c:Contract)-[:SIGNED_BY_VENDOR]->(v:Party)
RETURN v.name AS vendor,
       AVG(r.rate_amount) AS avg_rate,
       MAX(r.rate_amount) AS max_rate,
       MIN(r.rate_amount) AS min_rate
ORDER BY avg_rate DESC

