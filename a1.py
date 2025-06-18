from pydantic import BaseModel, Field
from typing import Literal

class EngagementProfile(BaseModel):
    engagement_model: Literal[
        "fixed-price",
        "time-and-materials",
        "managed service",
        "staff augmentation",
        "other"
    ] = Field(..., description="The commercial engagement model that defines how the contract is structured.")
    
    billing_basis: Literal[
        "milestone-based",
        "monthly retainer",
        "hourly",
        "deliverable-based",
        "other"
    ] = Field(..., description="The basis on which the vendor is paid for the services.")
    
    duration_model: Literal[
        "ongoing",
        "project-based",
        "long-term",
        "short-term",
        "ad hoc",
        "other"
    ] = Field(..., description="The time structure of the engagement.")

