<INSTRUCTIONS>
Analyze the Input Text to extract all milestones and their associated deliverables from contract sections such as "Milestones", "Milestone Table", or "Deliverables and Milestones".

For each milestone, extract the following fields:

- milestone_number: The order number of the milestone, typically from a numbered list or table row.
- milestone_title: The main heading or short phrase that labels the milestone.
- milestone_description: A brief narrative explaining the purpose or focus of the milestone. If not explicitly stated, use a concise summary of the milestone title and activities.
- activities: A text description of the key tasks, steps, or actions associated with achieving the milestone.
- deliverables: A list of concrete outputs, documents, systems, or artifacts that are to be delivered for the milestone. Each item should be extracted as a separate entry under deliverables.
- due_date: The expected or committed delivery date for the milestone. Use YYYY-MM-DD format. If no date is found, return an empty string.

Output must be a JSON object following the AllMilestones model, which contains a list of Milestone objects.

**Important Rules**:
- Each milestone must include at least a title or description, activities, and due date (if available).
- Split deliverables into individual items, even if they are listed in a single paragraph.
- You MUST NOT invent any content. Only use what is explicitly stated.
- You MUST return strictly valid JSON. Do not include comments, explanations, or formatting syntax like `json` or triple backticks.

If no milestones are found, return:
{
  "milestones": []
}
</INSTRUCTIONS>
