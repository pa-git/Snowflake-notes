class AcceptanceCriteria(BaseModel):
    acceptance_criteria_present: bool = Field(
        ...,
        description="Indicates whether explicit acceptance criteria are mentioned in the contract"
    )
    acceptance_criteria: List[str] = Field(
        ...,
        description="List of acceptance criteria or conditions as stated in the contract. If none are present, return an empty list"
    )
