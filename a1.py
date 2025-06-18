service_function_type: Literal[
    "operational support",
    "software development",
    "quality and testing",
    "consulting and advisory",
    "technical implementation",
    "data and analytics",
    "project delivery",
    "other"
] = Field(..., description="Primary functional nature of the service delivered under the contract.")
