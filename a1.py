for i, s in enumerate(data.get("slas", {}).get("service_slas", []), start=1):
    print(f"  - SLA #{i}")
