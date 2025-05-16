task: answer_user_question
description: >
  Answer the user's question using the metadata, conversation history, and optionally a Cypher query
  against the Neo4j knowledge graph.

rules:
  - Only generate read-only Cypher queries (no writes, updates, or deletes).
  - Do not include or return the Cypher query text.
  - If the required data is already available in the conversation history or context, do not generate a query.
  - If data must be retrieved, use the `execute_query` tool and return results as a Markdown table.
  - Do not wrap the Markdown table in triple backticks.

steps:
  - Step 1: Check if the answer can be found in the conversation history or metadata.
  - Step 2: If additional data is needed, generate a read-only Cypher query.
  - Step 3: Execute the query using the `execute_query` tool.
  - Step 4: Present the final result using a Markdown table (no code block).
