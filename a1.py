class GovernanceAndScopeModel(BaseModel):
    service_level_agreements: List[ServiceLevelAgreement]
    reporting_and_governance: ReportingAndGovernance
    engagement_scope: EngagementScope



class ContextualModel(BaseModel):
    divisions: List[Division]
    initiatives: List[Initiative]
    projects: List[Project]
    deliverables_and_invoices: List[DeliverableAndInvoice]
    parties: List[Party]
