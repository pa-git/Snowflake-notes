description: |
  Answer the question using the conversation history, metadata, or Neo4j knowledge graph if needed.

  <CONVERSATION_HISTORY>
  {conversation_history}
  </CONVERSATION_HISTORY>

  <LATEST_USER_INPUT>
  {user_input}
  </LATEST_USER_INPUT>

  <INSTRUCTIONS>
  - Use the information in the conversation history or metadata whenever possible.
  - Only generate a Cypher query if the required data is not already available.
  - Generate read-only Cypher queries only (no writes, updates, or deletes).
  - Do not include or return the Cypher query in your response.
  - Use the `execute_query` tool to run the query and retrieve results.
  - Present your response clearly in natural language.
  - Use a Markdown table for structured data if helpful, but never enclose it in triple backticks.
  </INSTRUCTIONS>

expected_output: |
  A clear, natural language response. Use a Markdown table for data when needed, but never include triple backticks or markdown code fences.
