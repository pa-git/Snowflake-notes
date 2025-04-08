import json

with open("overview.json") as f1, open("services_roles.json") as f2, open("governance_scope.json") as f3, open("contextual.json") as f4:
    overview = json.load(f1)
    services_roles = json.load(f2)
    governance_scope = json.load(f3)
    contextual = json.load(f4)

final_contract_json = {**overview, **services_roles, **governance_scope, **contextual}

# Optionally save it
with open("full_contract.json", "w") as fout:
    json.dump(final_contract_json, fout, indent=2)
