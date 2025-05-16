These are two separate relationships starting from the same Contract node — not a chained path through CanonicalDivision.
In Cypher, paths like (:A)-[:X]->(:B)-[:Y]->(:C) imply a continuous traversal.
But here, both IS_FOR_DIVISION and IS_WITH_VENDOR originate independently from Contract, so they require separate MATCH clauses.
