import json

def json_to_full_markdown_contract(data: dict) -> str:
    def section(title: str) -> str:
        return f"\n## {title}\n"

    def table(header: str, rows: list[tuple[str, str]]) -> str:
        output = section(header)
        output += "| Key | Value |\n|-----|-------|\n"
        for key, val in rows:
            output += f"| {key} | {val} |\n"
        return output

    def bullet_list(header: str, items: list[str]) -> str:
        output = section(header)
        for item in items:
            output += f"- {item}\n"
        return output

    def fee_breakdown_table(items: list[dict]) -> str:
        output = section("Fee Breakdown")
        output += "| Event | Fee |\n|-------|-----|\n"
        for item in items:
            output += f"| {item['event']} | {item['fee']} |\n"
        return output

    def list_of_objects(header: str, items: list[dict]) -> str:
        output = section(header)
        for i, item in enumerate(items, 1):
            output += f"\n### {header[:-1]} {i}\n"
            for k, v in item.items():
                output += f"- **{k.replace('_', ' ').capitalize()}**: {v}\n"
        return output

    markdown = f"# Contract Report\n\n**Summary:** {data['contract_metadata']['summary_description']}\n"

    markdown += table("Contract Metadata", [
        ("File Name", data["contract_metadata"]["file_name"]),
        ("Contract Type", data["contract_metadata"]["type"]),
        ("Start Date", data["contract_metadata"]["start_date"]),
        ("End Date", data["contract_metadata"]["end_date"]),
    ])

    fin = data["financials"]
    markdown += table("Financials", [
        ("Base Fee", fin["base_fee"]),
        ("Total Fee", fin["total_fee"]),
        ("Payment Terms", fin["payment_terms"]),
        ("Billing Instructions", fin["billing_instructions"]),
    ])
    markdown += fee_breakdown_table(fin["fee_breakdown"])
    markdown += bullet_list("Exclusions", fin["exclusions"])
    markdown += bullet_list("Exceptions or Notes", fin["exceptions_or_notes"])

    markdown += list_of_objects("Services", data.get("services", []))
    markdown += list_of_objects("Roles", data.get("roles", []))
    markdown += list_of_objects("Service Level Agreements", data.get("service_level_agreements", []))
    markdown += list_of_objects("Divisions", data.get("divisions", []))
    markdown += list_of_objects("Initiatives", data.get("initiatives", []))
    markdown += list_of_objects("Projects", data.get("projects", []))
    markdown += list_of_objects("Signatures", data.get("signatures", []))

    rg = data.get("reporting_and_governance", {})
    markdown += bullet_list("Reports", rg.get("reports", []))
    markdown += bullet_list("Meetings", rg.get("meetings", []))

    scope = data.get("engagement_scope", {})
    markdown += bullet_list("Core Applications", scope.get("core_applications", []))
    markdown += bullet_list("Supporting Applications", scope.get("supporting_applications", []))
    markdown += bullet_list("Key Activities", scope.get("key_activities", []))
    markdown += bullet_list("Assumptions", scope.get("assumptions", []))
    markdown += bullet_list("Expectations", scope.get("expectations", []))
    markdown += bullet_list("Conditions", scope.get("conditions", []))

    markdown += list_of_objects("Deliverables and Invoices", data.get("deliverables_and_invoices", []))
    markdown += list_of_objects("Parties", data.get("parties", []))

    return markdown


if __name__ == "__main__":
    with open("sample_contract.json", "r") as f:
        contract_data = json.load(f)
    markdown = json_to_full_markdown_contract(contract_data)
    with open("contract_report.md", "w") as f:
        f.write(markdown)
    print("✅ Markdown report generated: contract_report.md")
