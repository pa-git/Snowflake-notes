# Define the input schema for the contract search tool
class SearchToolInput(BaseModel):
    """Required fields for contract search; can be left empty when not used."""

    query: str = Field("", description="Search term for semantic search; leave empty to retrieve the full section")
    source: str = Field("", description="Contract name to filter by (e.g., 'Unified_Managed_Services_Contract_v5')")
    vendor: str = Field("", description="Vendor name to filter by (e.g., 'Ernst & Young LLP')")
    section: str = Field("", description="Section of the contract to search within (e.g., 'Roles', 'Services')")
