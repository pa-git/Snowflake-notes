text_reviewer:
  role: >
    Text Reviewer and Formatter for Contract Information
  goal: >
    Review the extracted text from the PDF, reformatting portions (especially those originating from data tables) to ensure the text is coherent and accurately reflects the original content.
  backstory: >
    You are experienced in identifying and correcting formatting issues, particularly with text extracted from images and tables. Your expertise ensures that the contract information is clear and logically organized.
  llm: openai/gpt-4o-mini

text_analyzer:
  role: >
    Contract Information Analyzer
  goal: >
    Analyze the reviewed text to extract all relevant contract details, including the nature of the service, skills provided, rates or unit price, rates by skills and location, conditions, responsibilities, delivery model, term, duration, and any other pertinent information, then output the data as JSON.
  backstory: >
    With a keen analytical mind, you excel at parsing complex contract language into structured data, ensuring that every essential detail is captured accurately.
  llm: openai/gpt-4o-mini

json_reviewer:
  role: >
    JSON Validator and Reviewer for Contract Information
  goal: >
    Validate and cross-check the JSON output against the reviewed text to ensure that no details were omitted or misinterpreted, and produce a final, verified JSON object.
  backstory: >
    Your meticulous review process guarantees that the extracted data is complete and accurate, providing a reliable final JSON representation of the contract details.
  llm: openai/gpt-4o-mini

markdown_generator:
  role: >
    Markdown Report Generator for Contract Information
  goal: >
    Convert the final JSON into a clear, well-organized markdown table, including a summary section at the top that highlights the key contract details.
  backstory: >
    You are skilled at transforming structured data into concise and visually appealing markdown reports that effectively communicate complex contract information.
  llm: openai/gpt-4o-mini








review_text:
  description: >
    Review the provided extracted text from the PDF. Reformat any portions that originate from data tables so that the text becomes coherent and accurately represents the original content.
  expected_output: >
    Reviewed text with improved formatting, particularly for sections that were originally in tables.
  agent: text_reviewer

analyze_text:
  description: >
    Analyze the reviewed text to extract all relevant contract details. Pay close attention to the nature of the service, skills provided, rates or unit price, rates by skills and location, conditions, responsibilities, delivery model, term, duration, and any other pertinent details.
  expected_output: >
    A JSON object containing all the extracted contract details.
  agent: text_analyzer
  context:
    - review_text

review_json:
  description: >
    Review the JSON output from the analysis and compare it with the reviewed text to ensure that all contract details are accurately captured. Correct any discrepancies to produce a final, verified JSON.
  expected_output: >
    A final, verified JSON object containing complete contract information.
  agent: json_reviewer
  context:
    - review_text
    - analyze_text

generate_markdown:
  description: >
    Convert the final JSON into a markdown table that organizes all the contract details. Include a summary section at the top that highlights the key information from the contract.
  expected_output: >
    A markdown document with a summary section and a detailed table presenting all the contract information.
  agent: markdown_generator
  context:
    - review_json








# src/contract_analyst_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ContractAnalystCrew():
    """Crew for analyzing contract information and generating a markdown report."""

    @agent
    def text_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['text_reviewer'],
            verbose=True
        )

    @agent
    def text_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['text_analyzer'],
            verbose=True
        )

    @agent
    def json_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['json_reviewer'],
            verbose=True
        )

    @agent
    def markdown_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['markdown_generator'],
            verbose=True
        )

    @task
    def review_text(self) -> Task:
        return Task(
            config=self.tasks_config['review_text']
        )

    @task
    def analyze_text(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_text']
        )

    @task
    def review_json(self) -> Task:
        return Task(
            config=self.tasks_config['review_json']
        )

    @task
    def generate_markdown(self) -> Task:
        return Task(
            config=self.tasks_config['generate_markdown'],
            output_file='output/contract_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Contract Analyst Crew for processing and reporting contract details."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )






