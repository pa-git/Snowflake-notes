from pydantic import BaseModel, Field
from typing import List, Literal

class MethodologyAndGovernance(BaseModel):
    methodology_keywords: List[
        Literal[
            "Agile",
            "Scrum",
            "Kanban",
            "Waterfall",
            "ITIL",
            "DevOps",
            "none",
            "other"
        ]
    ] = Field(
        ...,
        description="List of project delivery or governance methodologies explicitly mentioned in the contract"
    )
    team_management_structure: Literal[
        "vendor-led",
        "client-led",
        "shared",
        "unclear"
    ] = Field(
        ...,
        description="Indicates who is responsible for managing the day-to-day delivery of the work"
    )
