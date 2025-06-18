class Deliverable(BaseModel):
    description: str = Field(..., description="Description of the output or item delivered for this milestone.")

class Milestone(BaseModel):
    milestone_number: int = Field(..., description="The order number of the milestone.")
    milestone_title: str = Field(..., description="Title or label of the milestone.")
    milestone_description: str = Field(..., description="Short narrative of what this milestone is about.")
    activities: str = Field(..., description="List or description of activities required to reach this milestone.")
    deliverables: List[Deliverable] = Field(..., description="List of deliverables associated with this milestone.")
    due_date: date = Field(..., description="Expected delivery date of the milestone.")
