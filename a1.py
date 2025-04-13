json_data = [c.model_dump() for c in self.state['identify_use_case_task'].pydantic.changes]

json_data = [c.dict() for c in self.state['identify_use_case_task'].pydantic.changes]
