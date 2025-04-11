from pydantic import BaseModel, Field
from typing import Literal


class Drivers(BaseModel):
    """Driver of change"""

    transaction_type: Literal['increase', 'decrease'] = Field(
        ..., description="Direction of the change"
    )

    change_unit: Literal['percent', 'unit'] = Field(
        ..., description="Unit used to express the change"
    )

    change_quantity: int = Field(
        ..., description="Quantity of the change (without unit), e.g., 10"
    )

    division: Literal[
        'Cyber Data Risk & Resilience',
        'ENTERPRISE TECH & SERVICES',
        'Enterprise Tech & Svc ISGAlign',
        'Fin-Risk-Prog & Prod Eng Tech',
        'IM IT',
        'Innovation',
        'Institutional Securities Tech',
        'Tech COO',
        'WM Technology'
    ] = Field(
        ..., description="Division where the change applies"
    )

    resource_class: Literal['Permanent Employee', 'Contingent'] = Field(
        ..., description="Type of human resource affected"
    )

    location: Literal['high', 'medium', 'low'] = Field(
        ..., description="Location band impacted by the change"
    )

    year: int = Field(
        ..., description="Year the change starts"
    )

    month: int = Field(
        ..., description="Month the change starts"
    )
