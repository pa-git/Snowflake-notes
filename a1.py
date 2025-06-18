from typing import List, Literal
from pydantic import BaseModel, Field

class NonConformingResource(BaseModel):
    resource_description: str = Field(..., description="The name or description of the non-conforming resource (e.g., QA team, developer bench).")
    non_conformity_type: Literal["non-billable", "bench", "free"] = Field(..., description="The type of non-conforming status assigned to the resource.")

class NonConformingResourceDetection(BaseModel):
    non_conforming_resources: List[NonConformingResource] = Field(..., description="List of all non-conforming resources found in the contract.")
