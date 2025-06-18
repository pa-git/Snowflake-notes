from pydantic import BaseModel, Field
from typing import Literal

class EngagementProfileModel(BaseModel):
    engagement_model: Literal[
        "fixed-price", 
        "time-and-materials", 
        "managed service", 
        "staff augmentation"
    ] = Field(
        ...,
        description="The overall commercial model used for the engagement"
    )
    
    billing_basis: Literal[
        "milestone-based", 
        "monthly retainer", 
        "hourly", 
        "deliverable-based"
    ] = Field(
        ...,
        description="How the vendor is compensated for the work performed"
    )
    
    duration_model: Literal[
        "ongoing", 
        "long-term", 
        "project-based", 
        "ad hoc"
    ] = Field(
        ...,
        description="The temporal structure of the engagement"
    )
