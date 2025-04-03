# src/user_intent_analysis/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import AskUserTool

@CrewBase
class UserIntentAnalysisCrew():
  """Crew to classify and structure user intent using metadata"""

  @agent
  def senior_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['senior_analyst'],
      tools=[AskUserTool()],
      verbose=True
    )

  @task
  def identify_use_case_task(self) -> Task:
    return Task(
      config=self.tasks_config['identify_use_case_task']
    )

  @task
  def general_question_task(self) -> Task:
    return Task(
      config=self.tasks_config['general_question_task'],
      context=[self.identify_use_case_task()]
    )

  @task
  def data_question_intent_task(self) -> Task:
    return Task(
      config=self.tasks_config['data_question_intent_task'],
      context=[self.identify_use_case_task()]
    )

  @task
  def scenario_question_intent_task(self) -> Task:
    return Task(
      config=self.tasks_config['scenario_question_intent_task'],
      context=[self.identify_use_case_task()]
    )

  @crew
  def crew(self) -> Crew:
    """Creates the UserIntentAnalysis crew"""
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True
    )
