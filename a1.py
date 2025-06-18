from pydantic import BaseModel, Field
from typing import Literal

class BusinessContextModel(BaseModel):
    primary_goal: Literal[
        "advisory", 
        "modernization", 
        "operational continuity", 
        "upgrade", 
        "compliance", 
        "strategic planning", 
        "technical delivery", 
        "support"
    ] = Field(..., description="The main business purpose of the service being contracted. Select the most representative goal based on the contract's stated intent.")
    
    business_area: Literal[
        "infrastructure", 
        "application development", 
        "data and analytics", 
        "compliance and risk", 
        "automation", 
        "IT operations", 
        "enterprise architecture", 
        "cloud and platform engineering"
    ] = Field(..., description="The business or technical domain where the service is applied, based on the contract scope and language.")
