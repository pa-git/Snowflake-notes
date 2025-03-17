from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class POAnalystCrew():
    """Crew for analyzing purchase orders via multi-agent orchestration"""

    @agent
    def pdf_parser(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_parser'],
            verbose=True
        )

    @agent
    def data_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['data_extractor'],
            verbose=True
        )

    @agent
    def po_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['po_analyzer'],
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'],
            verbose=True
        )

    @task
    def extract_text(self) -> Task:
        return Task(
            config=self.tasks_config['extract_text']
        )

    @task
    def parse_po_details(self) -> Task:
        return Task(
            config=self.tasks_config['parse_po_details']
        )

    @task
    def analyze_po(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_po']
        )

    @task
    def review_data(self) -> Task:
        return Task(
            config=self.tasks_config['review_data']
        )

    @task
    def generate_report(self) -> Task:
        return Task(
            config=self.tasks_config['generate_report'],
            output_file='output/po_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Purchase Order Analyst Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )



######################################################################
######################################################################
######################################################################

pdf_parser:
  role: >
    PDF Parsing Specialist for Purchase Orders
  goal: >
    Extract accurate and complete raw text from purchase order PDF files
    to enable subsequent data extraction and analysis.
  backstory: >
    You are an efficient and reliable PDF parser with expertise in handling
    complex layouts and extracting necessary text from purchase order documents.
  llm: openai/gpt-4o-mini

data_extractor:
  role: >
    Data Extraction Specialist for Purchase Orders
  goal: >
    Parse the raw text to extract structured purchase order details such as
    PO numbers, dates, items, quantities, and prices.
  backstory: >
    You have deep knowledge of purchase order formats and excel at using pattern
    recognition and NLP techniques to convert unstructured text into structured data.
  llm: openai/gpt-4o-mini

po_analyzer:
  role: >
    Purchase Order Analysis Expert
  goal: >
    Analyze the structured purchase order data to identify discrepancies,
    compliance issues, and overall order health.
  backstory: >
    You are a meticulous analyst with strong attention to detail, experienced in
    financial data review, and skilled at flagging potential issues or anomalies.
  llm: openai/gpt-4o-mini

reviewer:
  role: >
    Quality Assurance Reviewer for Purchase Orders
  goal: >
    Validate the extracted data and analysis results, ensuring accuracy and
    consistency throughout the purchase order report.
  backstory: >
    You are an experienced reviewer known for catching errors and ensuring that
    all data meets the highest quality standards before final reporting.
  llm: openai/gpt-4o-mini

report_generator:
  role: >
    Purchase Order Report Generator
  goal: >
    Compile all processed data into a clear, comprehensive, and well-structured
    report for stakeholders.
  backstory: >
    With expertise in technical writing and data presentation, you transform
    complex analysis into accessible insights that inform decision making.
  llm: openai/gpt-4o-mini


###################################################################################################################


extract_text:
  description: >
    Extract raw text from the purchase order PDF. Ensure that the extraction handles
    various layouts and captures all content accurately.
  expected_output: >
    A plain text version of the purchase order, capturing all text content from the PDF.
  agent: pdf_parser

parse_po_details:
  description: >
    Parse the extracted text to identify key purchase order details including PO number,
    date, vendor information, and a detailed itemized list (with quantities and prices).
  expected_output: >
    Structured data (e.g., in JSON format) containing the purchase order details.
  agent: data_extractor
  context:
    - extract_text

analyze_po:
  description: >
    Analyze the structured purchase order data for consistency and potential issues.
    This includes verifying totals, identifying discrepancies, and ensuring compliance.
  expected_output: >
    An analysis summary that includes computed totals, flagged issues, and a compliance check.
  agent: po_analyzer
  context:
    - parse_po_details

review_data:
  description: >
    Review the extracted data and analysis to validate accuracy and consistency.
    Ensure that all details conform to expected standards and highlight any anomalies.
  expected_output: >
    A review report indicating whether the data is approved and noting any required adjustments.
  agent: reviewer
  context:
    - parse_po_details
    - analyze_po

generate_report:
  description: >
    Compile the purchase order details, analysis, and reviewer feedback into a comprehensive report.
    The report should be clear, well-organized, and formatted for stakeholder review.
  expected_output: >
    A final report document that summarizes the purchase order, analysis findings, and review comments.
  agent: report_generator
  context:
    - parse_po_details
    - analyze_po
    - review_data
  output_file: output/po_report.md

