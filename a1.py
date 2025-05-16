def run_cypher_query(query: str):
    results, meta = db.cypher_query(query)
    headers = [col[0] if col[0] else f"col{i}" for i, col in enumerate(meta)]
    return [dict(zip(headers, row + [None] * (len(headers) - len(row)))) for row in results]
