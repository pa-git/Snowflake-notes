def run_cypher_query(query: str):
    results, meta = db.cypher_query(query)
    headers = [col[0] for col in meta]
    return [dict(zip(headers, row + [None] * (len(headers) - len(row)))) for row in results]
