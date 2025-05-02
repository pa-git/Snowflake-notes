def normalize_section_name(original_name: str) -> str:
    """
    Map specific section names to normalized group names.
    """

    mapping = {
        "Financials": "Financials",
        "Fee Breakdown": "Financials",
        "Exclusions": "Financials",
        "Exceptions or Notes": "Financials",

        "Divisions": "Scope and Structure",
        "Initiatives": "Scope and Structure",
        "Projects": "Scope and Structure",

        "Core Applications": "Applications and Expectations",
        "Supporting Applications": "Applications and Expectations",
        "Key Activities": "Applications and Expectations",
        "Assumptions": "Applications and Expectations",
        "Expectations": "Applications and Expectations",
        "Conditions": "Applications and Expectations",

        "Contract Metadata": "Contract Metadata",
        "Parties": "Contract Metadata",
    }

    return mapping.get(original_name.strip(), original_name)



normalized_name = normalize_section_name(section.metadata.get("section", ""))
section.metadata = {
    "source": filename,
    "vendor": vendor_name,
    "section": normalized_name,
    **section.metadata
}
