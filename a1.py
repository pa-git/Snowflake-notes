task: answer_user_question
description: >
  Answer the user's question using the metadata, conversation history, and optionally a Cypher query
  against the Neo4j knowledge graph.

rules:
  - Only generate read-only Cypher queries (no writes, updates, or deletes).
  - Do not include or return the Cypher query text in your final response.
  - If the required data is already available in the conversation history or context, do not generate a query.
  - If additional data is needed, use the `execute_query` tool to retrieve it.
  - Always present your full response in natural language, supported by a Markdown table if needed (but never inside triple backticks).

steps:
  - Step 1: Check if the answer is already available from the conversation history or metadata.
  - Step 2: If additional data is needed, generate a read-only Cypher query to retrieve it.
  - Step 3: Use the `execute_query` tool to run the query and fetch the result.
  - Step 4: Present a complete, clear, and context-aware response. Use a Markdown table to support the answer when appropriate, without enclosing it in code blocks.
