from typing import Literal, Optional
from pydantic import BaseModel, Field

class TravelAndExpenseDetail(BaseModel):
    description: str = Field(..., description="Description of the travel and expense terms as stated in the contract.")
    fee_type: Literal["reimbursable", "non-reimbursable", "pass-through"] = Field(..., description="The type of T&E fee as classified in the contract.")
    cap_amount: Optional[float] = Field(None, description="Maximum reimbursable or allowable amount for T&E, if a cap is defined.")
    currency: Optional[str] = Field(None, description="Currency in which the T&E cap or costs are stated (e.g., USD, EUR).")
    billing_method: Optional[Literal["actuals", "per diem", "estimated"]] = Field(None, description="The method by which T&E costs are calculated or billed.")
    approval_required: Optional[bool] = Field(None, description="Whether prior approval is required for the T&E to be reimbursed.")
