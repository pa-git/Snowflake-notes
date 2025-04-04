from pydantic import BaseModel, Field
from typing import List


class ContractMetadata(BaseModel):
    file_name: str = Field(..., description="The name of the contract file")
    type: str = Field(..., description="Type of contract, e.g., Purchase order")
    summary_description: str = Field(..., description="Summary of the contract content")
    start_date: str = Field(..., description="Start date of the contract")
    end_date: str = Field(..., description="End date of the contract")


class FeeBreakdownItem(BaseModel):
    event: str = Field(..., description="Name or description of the milestone/event")
    fee: str = Field(..., description="Fee associated with the event")


class Financials(BaseModel):
    base_fee: str = Field(..., description="Base fee amount in currency")
    total_fee: str = Field(..., description="Total fee amount in currency")
    fee_breakdown: List[FeeBreakdownItem] = Field(..., description="Detailed breakdown of fees")
    exclusions: List[str] = Field(..., description="Items excluded from fees")
    payment_terms: str = Field(..., description="Terms of payment")
    billing_instructions: str = Field(..., description="Billing instructions provided by the client")
    exceptions_or_notes: List[str] = Field(..., description="Any exceptions or additional notes")


class Service(BaseModel):
    name: str = Field(..., description="Name of the service")
    description: str = Field(..., description="Service description")
    period: str = Field(..., description="Service period")
    coverage: str = Field(..., description="Coverage type")
    locations: List[str] = Field(..., description="List of locations for the service")
    days: int = Field(..., description="Number of service days")
    quantity: int = Field(..., description="Quantity of service units")
    unit_price: str = Field(..., description="Unit price in currency")
    total: str = Field(..., description="Total amount for this service")
    notes: List[str] = Field(..., description="Additional service notes")


class Rate(BaseModel):
    amount: float = Field(..., description="Rate amount")
    currency: str = Field(..., description="Currency of the rate")
    unit: str = Field(..., description="Unit of rate, e.g., hour")


class Role(BaseModel):
    role_name: str = Field(..., description="Name of the role")
    resource_name: str = Field(..., description="Name of the resource assigned")
    description: str = Field(..., description="Role description")
    level: str = Field(..., description="Skill or seniority level")
    location: str = Field(..., description="Location of the role")
    hours_committed: int = Field(..., description="Number of hours committed")
    rate: Rate = Field(..., description="Rate details")
    total_fees: float = Field(..., description="Total fees for the role")
    billing_type: str = Field(..., description="Type of billing method")
    schedule_reference: str = Field(..., description="Schedule document reference")
    project: str = Field(..., description="Associated project name")


class ServiceLevelAgreement(BaseModel):
    name: str = Field(..., description="Name of the SLA")
    description: str = Field(..., description="SLA description")
    target: str = Field(..., description="SLA target goal")
    metric: str = Field(..., description="Metric used to measure the SLA")
    unit: str = Field(..., description="Unit of measurement")
    frequency: str = Field(..., description="Frequency of SLA measurement")
    applies_to_services: List[str] = Field(..., description="Services the SLA applies to")
    penalty_clause: str = Field(..., description="Indicates if penalties apply")
    enforcement_method: str = Field(..., description="Method of enforcement")


class Division(BaseModel):
    name: str = Field(..., description="Division name")
    description: str = Field(..., description="Division description")


class Initiative(BaseModel):
    name: str = Field(..., description="Initiative name")
    description: str = Field(..., description="Initiative description")


class Project(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    start_date: str = Field(..., description="Project start date")
    end_date: str = Field(..., description="Project end date")
    division: str = Field(..., description="Associated division")
    initiative: str = Field(..., description="Associated initiative")
    status: str = Field(..., description="Project status")


class Signature(BaseModel):
    type: str = Field(..., description="Type of signee")
    name: str = Field(..., description="Name of signee")
    title: str = Field(..., description="Title of signee")
    date: str = Field(..., description="Date of signature")


class ReportingAndGovernance(BaseModel):
    reports: List[str] = Field(..., description="Types of reports included")
    meetings: List[str] = Field(..., description="Types of governance meetings")


class EngagementScope(BaseModel):
    core_applications: List[str] = Field(..., description="Core applications included in scope")
    supporting_applications: List[str] = Field(..., description="Supporting applications")
    key_activities: List[str] = Field(..., description="Key activities under engagement")
    assumptions: List[str] = Field(..., description="Assumptions underlying the engagement")
    expectations: List[str] = Field(..., description="Expectations of client/vendor")
    conditions: List[str] = Field(..., description="Conditions governing the engagement")


class DeliverableAndInvoice(BaseModel):
    deliverable: str = Field(..., description="Name of the deliverable")
    delivery_date: str = Field(..., description="Date of delivery")
    invoice_amount_usd: float = Field(..., description="Invoice amount in USD")
    percentage: float = Field(..., description="Percentage of total or milestone")


class Party(BaseModel):
    type: str = Field(..., description="Type of party, e.g., client or vendor")
    name: str = Field(..., description="Name of the party")
    address: str = Field(..., description="Party's address")
    context: str = Field(..., description="Contextual notes about the party")


class Contract(BaseModel):
    contract_metadata: ContractMetadata
    financials: Financials
    services: List[Service]
    roles: List[Role]
    service_level_agreements: List[ServiceLevelAgreement]
    divisions: List[Division]
    initiatives: List[Initiative]
    projects: List[Project]
    signatures: List[Signature]
    reporting_and_governance: ReportingAndGovernance
    engagement_scope: EngagementScope
    deliverables_and_invoices: List[DeliverableAndInvoice]
    parties: List[Party]
