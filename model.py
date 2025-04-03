from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class ContractMetadata(BaseModel):
    file_name: str = Field(..., description="Name of the contract file")
    type: str = Field(..., description="Type of contract (e.g., Purchase order)")
    summary_description: str = Field(..., description="Summary of the contract's purpose and contents")
    start_date: date = Field(..., description="Contract start date")
    end_date: date = Field(..., description="Contract end date")
    condition: str = Field(..., description="Condition under which the contract expires")


class FeeBreakdownItem(BaseModel):
    event: str = Field(..., description="Name or description of the billing milestone")
    fee: str = Field(..., description="Fee associated with the milestone")


class Financials(BaseModel):
    base_fee: str = Field(..., description="Initial or base fee for the engagement")
    adjusted_total_fee: str = Field(..., description="Total fee after adjustments")
    fee_breakdown: List[FeeBreakdownItem] = Field(..., description="Detailed fee milestones")
    excludes: List[str] = Field(..., description="Items excluded from the financial agreement")
    payment_terms: str = Field(..., description="Terms of payment as agreed upon")
    billing_instructions: str = Field(..., description="Instructions for how billing should be processed")
    exceptions_or_notes: List[str] = Field(..., description="Special notes or exceptions related to financials")


class ServiceItem(BaseModel):
    name: str = Field(..., description="Name of the service or role")
    details: str = Field(..., description="Description of the service provided")
    period: str = Field(..., description="Service duration period")
    coverage: str = Field(..., description="Coverage terms for service")
    locations: List[str] = Field(..., description="List of service delivery locations")
    days: int = Field(..., description="Number of days of service")
    quantity: int = Field(..., description="Quantity of service units")
    unit_price: str = Field(..., description="Price per unit")
    total: str = Field(..., description="Total cost for the service")
    notes: Optional[str] = Field(None, description="Any additional notes about the service")


class Rate(BaseModel):
    amount: float = Field(..., description="Hourly or unit amount")
    currency: str = Field(..., description="Currency used for billing")
    unit: str = Field(..., description="Unit type for billing (e.g., hour)")


class RoleItem(BaseModel):
    resource_name: str = Field(..., description="Name of the resource or person assigned")
    role_name: str = Field(..., description="Role or title of the person")
    description: str = Field(..., description="Description of responsibilities")
    level: str = Field(..., description="Skill or seniority level")
    location: str = Field(..., description="Geographic location of the resource")
    hours_committed: int = Field(..., description="Number of hours committed to the project")
    rate: Rate = Field(..., description="Rate structure for the resource")
    total_fees: float = Field(..., description="Total fees for the resource")
    billing_type: str = Field(..., description="Billing method (e.g., Time & Materials)")
    schedule_reference: str = Field(..., description="Reference to the contract schedule")
    project: str = Field(..., description="Project name or code associated with this role")


class SLAItem(BaseModel):
    name: str = Field(..., description="Name of the service level agreement (SLA)")
    description: str = Field(..., description="Description of the SLA metric")
    target: str = Field(..., description="Target performance level")
    metric: str = Field(..., description="Performance metric being measured")
    unit: str = Field(..., description="Unit of measure")
    frequency: str = Field(..., description="Frequency of measurement")
    applies_to_services: List[str] = Field(..., description="List of services this SLA applies to")
    penalty_clause: str = Field(..., description="Whether a penalty clause applies")
    enforcement_method: str = Field(..., description="How the SLA is enforced")


class Division(BaseModel):
    name: str = Field(..., description="Name of the division")
    description: str = Field(..., description="Division's function or scope")


class Initiative(BaseModel):
    name: str = Field(..., description="Initiative name")
    description: str = Field(..., description="Purpose or goal of the initiative")


class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Brief description of the project")
    start_date: date = Field(..., description="Project start date")
    end_date: date = Field(..., description="Project end date")
    division: str = Field(..., description="Division associated with the project")
    initiative: str = Field(..., description="Initiative this project supports")
    status: str = Field(..., description="Current status of the project")


class Signature(BaseModel):
    type: str = Field(..., description="Type of signee (e.g., consultant, client)")
    name: str = Field(..., description="Name of the person signing")
    title: str = Field(..., description="Title or role of the signee")
    date: date = Field(..., description="Date of signature")


class ReportingAndGovernance(BaseModel):
    reports: List[str] = Field(..., description="Types of reports to be delivered")
    meetings: List[str] = Field(..., description="Meeting cadences and types")


class EngagementScope(BaseModel):
    core_applications: List[str] = Field(..., description="Primary applications involved")
    supporting_applications: List[str] = Field(..., description="Secondary or supporting applications")
    key_activities: List[str] = Field(..., description="Key activities in scope")
    assumptions: List[str] = Field(..., description="Assumptions made regarding the engagement")
    expectations: List[str] = Field(..., description="Expectations from both parties")
    special_conditions: List[str] = Field(..., description="Special or non-standard terms")


class DeliverableInvoice(BaseModel):
    deliverable: str = Field(..., description="Name or description of the deliverable")
    delivery_date: date = Field(..., description="Date the deliverable is due or delivered")
    invoice_amount_usd: float = Field(..., description="Amount billed for this deliverable in USD")
    percentage: float = Field(..., description="Percentage of total this invoice represents")


class Party(BaseModel):
    type: str = Field(..., description="Party type (e.g., client, vendor)")
    name: str = Field(..., description="Name of the party")
    address: str = Field(..., description="Physical address of the party")
    context: Optional[str] = Field(None, description="Additional context or scope limitation")


class ContractModel(BaseModel):
    contract_metadata: ContractMetadata
    financials: Financials
    services: List[ServiceItem]
    roles: List[RoleItem]
    service_level_agreements: List[SLAItem]
    divisions: List[Division]
    initiatives: List[Initiative]
    projects: List[Project]
    signatures: List[Signature]
    reporting_and_governance: ReportingAndGovernance
    engagement_scope: EngagementScope
    deliverables_and_invoices: List[DeliverableInvoice]
    parties: List[Party]
