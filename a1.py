from pydantic import BaseModel, Field


class IdentifyUsecaseTaskOutput(BaseModel):
    """Identify Use Case Task Output"""

    use_case_id: str = Field(
        ..., 
        description="One of: 'general', 'data', 'scenario', 'clarification'"
    )
    use_case: str = Field(
        ..., 
        description="One of: 'General question', 'Data question', 'Scenario question', 'Clarification question'"
    )
    clarification_question: str = Field(
        ..., 
        description="Clarification question to ask the user, or 'None' if no clarification is needed"
    )
    restated_user_intent: str = Field(
        ..., 
        description="A clear restatement of the user's intent, including all necessary details required to support the next step of processing"
    )
