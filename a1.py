from pydantic import BaseModel, Field
from typing import Literal

class GovernanceMethodologyModel(BaseModel):
    methodology_keywords: str = Field(
        description="Text extracted from the contract listing the delivery methodology terms mentioned, such as Agile, Waterfall, ITIL, or others"
    )
    milestone_defined: Literal["yes", "no"] = Field(
        description="Indicates whether the contract explicitly defines project or delivery milestones"
    )
    acceptance_criteria_defined: Literal["yes", "no"] = Field(
        description="Indicates whether the contract includes formal acceptance criteria for deliverables"
    )
    team_management_structure: Literal["vendor-led", "client-led", "shared", "not specified"] = Field(
        description="Describes who is responsible for managing the delivery team on a day-to-day basis"
    )
