task: Group role titles into predefined Role Groups

description: >
  Analyze the list of role titles and group them according to the closest matching Role Group.
  Each title must be assigned to exactly one group. Use "Not Applicable" for personal names or entries
  that do not represent actual role titles.

output_format:
  type: array
  item:
    role_group: string  # Must be one of the provided ROLE_GROUP values
    matches:            # List of matching role titles for this group
      type: array
      items: string

rules:
  - Only use ROLE_GROUP values from the provided list
  - Assign every role title to exactly one group
  - Choose the closest semantic match for each title
  - Use "Not Applicable" for:
      - Personal names (e.g., "John Doe", "Swapnil Gupta")
      - Entries that clearly do not represent job roles
  - Do not invent new group names or modify existing ones
