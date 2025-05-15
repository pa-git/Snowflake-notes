from neomodel import db

def run_cypher_query(query: str):
    """
    Executes a raw Cypher query and returns the result as a list of dictionaries.

    Args:
        query (str): The Cypher query to run.

    Returns:
        List[Dict[str, Any]]: Query results as list of dictionaries.
    """
    results, meta = db.cypher_query(query)
    headers = [col[0] for col in meta]
    return [dict(zip(headers, row)) for row in results]
