class ExecuteQueryTaskInput(BaseModel):
    analysis_plan: str = Field(..., description="Instructions describing how to process and analyze the retrieved content")
    query: Optional[str] = Field("", description="Search term for semantic search; empty if retrieving full section")
    source: Optional[str] = Field(None, description="Contract name to filter by (e.g., 'Unified_Managed_Services_Contract_v5')")
    vendor: Optional[str] = Field(None, description="Vendor name to filter by (e.g., 'Ernst & Young LLP')")
    section: str = Field(..., description="Specific section of the contract to search within (e.g., 'Roles', 'Services')")
