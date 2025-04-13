json_data = [
    {**c.dict(), "source": "LLM"}
    for c in self.state['identify_use_case_task'].pydantic.changes
]
