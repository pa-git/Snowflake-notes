<INSTRUCTIONS>
Analyze the input text to extract all relevant information related to the nature of the service delivered and how it is delivered under the contract.

You must return the following five fields, using the exact format and wording described below:

- service_summary: A concise plain-language summary (2–4 sentences) describing the service. It should reflect what the vendor is doing, for whom, and for what purpose. Use simple language and avoid jargon. Example: "The vendor will provide ongoing support for the client's internal applications, including bug fixes, minor enhancements, and operational troubleshooting."

- service_function_type: Identify the primary purpose of the service. Choose one of the following values:
  • "operational support" – for services such as application support, maintenance, release management, or production operations.
  • "software engineering" – for contracts focused on development, coding, or technical build of applications.
  • "quality assurance" – for services involving functional testing, test automation, UAT, or validation work.
  • "advisory consulting" – for strategy, analysis, business process review, or architecture without hands-on build.
  • "technical implementation" – for hands-on system configuration or platform enablement without full custom development.
  • "system integration" – for connecting multiple platforms or orchestrating cross-system workflows.
  • "application modernization" – for upgrading, refactoring, or replatforming existing applications.
  • "project management" – if the service is primarily for managing or overseeing delivery.
  • "other" – if the function doesn’t match any above; use only as a last resort.

- includes_development_work: A boolean value indicating whether the contract scope includes technical development or hands-on software build.
  • Return true if any part of the service includes writing, modifying, or delivering code.
  • Return false if the service is limited to consulting, management, support, or testing without code delivery.

- focus_area_keywords: A list of relevant terms or phrases that describe the focus of the service.
  • Extract up to 10 keywords or phrases that indicate the technologies, systems, or domains in scope.
  • Examples include "application support", "cloud migration", "QA automation", "data pipelines", "SAP", "mainframe", etc.

- delivery_model: Identify how the work is delivered and organized. Choose one of the following:
  • "dedicated team" – if the vendor provides a stable team working consistently over time.
  • "centralized help desk" – if the service is structured around a queue- or ticket-based resolution model.
  • "on-demand tickets" – if resources are pulled in reactively as needed without a permanent assignment.
  • "individual contributors" – if delivery is done by a single person or separate individuals working independently.
  • "staff augmentation" – if resources are placed into the client’s existing team to operate under their supervision.
  • "hybrid" – if the contract explicitly mixes models (e.g., some dedicated roles, some ticket-based support).
  • "other" – if no model fits clearly.

Return the output as a JSON object strictly following the field names and types defined above.

</INSTRUCTIONS>
