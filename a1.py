from pydantic import BaseModel, Field
from typing import Literal, List


class IdentifyUsecaseTaskOutput(BaseModel):
    """Identify Use Case Task Output"""
    use_case_id: Literal['general', 'data', 'scenario', 'clarification'] = Field(..., description="Type of question the user is asking")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")
    restated_user_intent: str = Field(..., description="A clear restatement of the user's intent, including all available details")


class GeneralQuestionTaskOutput(BaseModel):
    """General Question Task Output"""
    use_case_id: Literal['general', 'clarification'] = Field(..., description="Type of question being answered")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")
    answer: str = Field(..., description="A direct answer to the user's question")


class DataQuestionIntentTaskOutput(BaseModel):
    """Data Question Intent Task Output"""
    use_case_id: Literal['data', 'clarification'] = Field(..., description="Type of question being answered")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")
    user_intent: str = Field(..., description="User intent based on the question asked")
    required_tables_and_columns: str = Field(..., description="Required tables and columns to answer the question")
    joins: str = Field(..., description="Join conditions between tables")
    filters: str = Field(..., description="Filter conditions to be applied")
    aggregations: str = Field(..., description="Aggregations to be applied")


class Drivers(BaseModel):
    """Driver of change"""
    transaction_type: Literal['increase', 'decrease'] = Field(..., description="Direction of the change")
    change_unit: Literal['percent', 'unit'] = Field(..., description="Unit used to express the change")
    change_quantity: int = Field(..., description="Quantity of the change (without unit), e.g., 10")
    division: Literal[
        'Cyber Data Risk & Resilience',
        'ENTERPRISE TECH & SERVICES',
        'Enterprise Tech & Svc ISGAlign',
        'Fin-Risk-Prog & Prod Eng Tech',
        'IM IT',
        'Innovation',
        'Institutional Securities Tech',
        'Tech COO',
        'WM Technology'
    ] = Field(..., description="Division where the change is applied")
    resource_class: Literal['Permanent Employee', 'Contingent'] = Field(..., description="Type of human resource affected")
    location: Literal['high', 'medium', 'low'] = Field(..., description="Location category impacted by the change")
    year: int = Field(..., description="Year the change starts")
    month: int = Field(..., description="Month the change starts")


class ScenarioQuestionIntentTaskOutput(BaseModel):
    """Scenario Question Intent Task Output"""
    use_case_id: Literal['scenario', 'clarification'] = Field(..., description="Type of question being answered")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")
    changes: List[Drivers] = Field(..., description="List of changes to be made in the scenario")
