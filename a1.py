description: |
  <CONVERSATION_HISTORY>
  {conversation_history}
  </CONVERSATION_HISTORY>

  <LATEST_USER_INPUT>
  {user_input}
  </LATEST_USER_INPUT>

  <INSTRUCTIONS>
  Answer the question using the conversation history, metadata, or Neo4j knowledge graph if needed.

  - Use the conversation history and metadata whenever possible.
  - Only generate a Cypher query if the required data is not already available.
  - Only generate read-only Cypher queries (no writes, updates, or deletes).
  - Do not include or return the Cypher query text in your response.
  - Use the `execute_query` tool to run the query and retrieve results if needed.
  - Present your full response clearly in natural language.
  - Use a Markdown table for structured data if helpful, but never use triple backticks or code fences.
  </INSTRUCTIONS>

expected_output: |
  A complete, clear, and context-aware response in natural language. Use a Markdown table to present structured data when appropriate, without using triple backticks.
