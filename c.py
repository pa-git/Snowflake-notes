# src/query_execution/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import AskUserTool

@CrewBase
class QueryExecutionCrew():
  """Crew that builds and executes SQL SELECT queries using metadata and user intent"""

  @agent
  def query_builder_executor(self) -> Agent:
    return Agent(
      config=self.agents_config['query_builder_executor'],
      tools=[AskUserTool()],
      verbose=True
    )

  @task
  def build_execute_query(self) -> Task:
    return Task(
      config=self.tasks_config['build_execute_query']
    )

  @crew
  def crew(self) -> Crew:
    """Creates the QueryExecution crew"""
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True
    )


-------------------------------


query_builder_executor:
  role: "Expert {dialect} SQL Query Builder and Executor"
  goal: >
    Build a syntactically correct and effective SELECT query using the {dialect} SQL dialect,
    based on detailed user requirements and metadata. Then execute the query and return the results.
  backstory: >
    You are a highly experienced SQL expert specializing in the {dialect} SQL dialect.
    Your role is to transform structured user requirements into optimized and executable SELECT statements.
    You never guess or assume information — instead, you clarify any uncertainty using the ask_question tool.
    You strictly follow metadata definitions and always return the query result (not the query itself),
    formatted as a Markdown table for user readability.


-----------------------



build_execute_query:
  description: >
    Using the detailed user intent and metadata, construct the required {dialect} SELECT SQL query following the steps below,
    then execute your query using the `execute_query` tool.

    **IMPORTANT**:
    - You can only create SELECT queries.
    - You can only respond with the Data returned by the `execute_query` tool, formatted as a table using Markdown.
    - You never respond with the query itself.

    You MUST use the `ask_question` tool if anything is unclear — including metadata, intent, join conditions, filters, or expected fields.
    Never assume or fabricate schema, table, or column names.

    # Metadata:
    ```{metadata}```

    # Follow these steps:
    1. Understand the metadata.
    2. Understand the user intent from the prior analysis.
    3. Determine if joins are required; specify the type (INNER JOIN, LEFT JOIN, etc.).
    4. Identify filters needed. Only use sample values from metadata—do NOT invent values.
    5. Decide which columns to include in the SELECT clause.
    6. Assemble the full query string.
    7. Finally, execute your final query using the `execute_query` tool.

    After running the query:
    - If the query returns errors, analyze and revise accordingly.
    - If the query succeeds, return the results formatted as a Markdown table.

    **Query rules**:
    - ALWAYS include both the schema and table names in the format SCHEMA.TABLE (e.g., SELECT * FROM SCHEMA.TABLE).
    - ALWAYS execute your final query using the `execute_query` tool.
  expected_output: A Markdown table. Do not include triple backticks or 'markdown' in your response.
  agent: query_builder
  context: [analyze_user_input]

