Group the following role names into the appropriate Role Groups.

Return the result as a JSON object, where each key is a ROLE_GROUP (from the provided list), and the value is a list of matching role names.

You must assign each role to one of the available categories. Choose the closest match based on role semantics. Only use "Other" if no reasonable match can be found.

Example Output:

json
Copy
Edit
{
  "Technology Management": [
    "Project Management",
    "Senior PM/Scrum Master",
    "Senior Business Analyst",
    "Product Manager"
  ]
}
Important: You must only use ROLE_GROUP values from the provided list. Do not invent new categories.
