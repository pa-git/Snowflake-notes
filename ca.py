class Filters(BaseModel):
    source: Optional[str] = Field(None, description="Contract document name (e.g., 'Unified_Managed_Services_Contract_v5')")
    vendor: Optional[str] = Field(None, description="Vendor name (e.g., 'Ernst & Young LLP')")
    section: Optional[str] = Field(None, description="Contract section of interest (e.g., 'Roles')")

class AnalyzeQueryTaskOutput(BaseModel):
    analysis_plan: str = Field(..., description="High-level plan to answer the user question")
    query: Optional[str] = Field("", description="Search term for semantic query; leave empty if pulling full section")
    filters: Filters = Field(..., description="Contract filters including source, vendor, and section")
