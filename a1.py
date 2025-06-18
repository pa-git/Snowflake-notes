from pydantic import BaseModel, Field
from typing import List, Literal

class ToolAndPlatformExtraction(BaseModel):
    tool_types_mentioned: List[
        Literal[
            "test automation",
            "CI/CD",
            "data pipeline tools",
            "ETL tools",
            "business intelligence tools",
            "APIs",
            "source control tools",
            "performance monitoring tools",
            "cloud infrastructure tools",
            "project management tools",
            "other"
        ]
    ] = Field(
        ...,
        description="List of specific tool categories explicitly mentioned in the contract, selected from a predefined list"
    )
    
    platform_scope: List[
        Literal[
            "web",
            "mobile",
            "embedded",
            "mainframe",
            "cloud",
            "on-premise",
            "distributed systems",
            "other"
        ]
    ] = Field(
        ...,
        description="List of platforms covered by the service as explicitly referenced in the contract"
    )
