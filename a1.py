from pydantic import BaseModel, Field
from typing import List, Literal

class ScopeDeliveryModel(BaseModel):
    service_function_type: Literal[
        "operational support",
        "software engineering",
        "quality assurance",
        "advisory consulting",
        "technical implementation",
        "system integration",
        "application modernization",
        "project management",
        "other"
    ] = Field(..., description="Primary function of the service delivered under the contract.")

    includes_development_work: Literal[True, False] = Field(
        ..., description="Whether the service includes hands-on development, coding, or solution delivery."
    )

    focus_area_keywords: List[str] = Field(
        ..., description="List of key topics or terms indicating the technical or business focus of the service."
    )

    delivery_model: Literal[
        "dedicated team",
        "centralized help desk",
        "on-demand tickets",
        "individual contributors",
        "staff augmentation",
        "hybrid",
        "other"
    ] = Field(..., description="How the service is delivered and organized from a staffing and structure perspective.")
