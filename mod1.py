from pydantic import BaseModel, Field
from typing import List


class IdentifyUsecaseTaskOutput(BaseModel):
    """Identify Use Case Task Output"""
    use_case_id: str = Field(..., description="One of: 'general', 'data', 'scenario', 'clarification'")
    use_case: str = Field(..., description="One of: 'General question', 'Data question', 'Scenario question', 'Clarification question'")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")


class GeneralQuestionTaskOutput(BaseModel):
    """General Question Task Output"""
    use_case_id: str = Field(..., description="One of: 'general', 'data', 'scenario', 'clarification'")
    use_case: str = Field(..., description="One of: 'General question', 'Data question', 'Scenario question', 'Clarification question'")
    answer: str = Field(..., description="A direct answer to the user's question")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")


class DataQuestionIntentTaskOutput(BaseModel):
    """Data Question Intent Task Output"""
    use_case_id: str = Field(..., description="One of: 'general', 'data', 'scenario', 'clarification'")
    use_case: str = Field(..., description="One of: 'General question', 'Data question', 'Scenario question', 'Clarification question'")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")
    user_intent: str = Field(..., description="User intent based on the question asked")
    required_tables_and_columns: str = Field(..., description="Required tables and columns to answer the question")
    joins: str = Field(..., description="Join conditions between tables")
    filters: str = Field(..., description="Filter conditions to be applied")
    aggregations: str = Field(..., description="Aggregations to be applied")


class Drivers(BaseModel):
    """Driver of change"""
    change_type: str = Field(..., description="Change type to be applied")
    change_unit: str = Field(..., description="Change unit to be applied")
    change_quantity: str = Field(..., description="Change quantity to be applied")
    organization: str = Field(..., description="Organization to be applied")
    resources: str = Field(..., description="Resources to be applied")
    location: str = Field(..., description="Location to be applied")


class ScenarioQuestionIntentTaskOutput(BaseModel):
    """Scenario Question Intent Task Output"""
    use_case_id: str = Field(..., description="One of: 'scenario', 'clarification'")
    use_case: str = Field(..., description="One of: 'Scenario question', 'Clarification question'")
    clarification_question: str = Field(..., description="Clarification question to ask the user, or 'None' if no clarification is needed")
    changes: List[Drivers] = Field(..., description="List of changes to be made in the scenario")
