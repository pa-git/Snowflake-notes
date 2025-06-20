from models import Service, CanonicalService
from neomodel import db

def get_distinct_service_function_types():
    query = """
    MATCH (s:Service)
    WHERE s.service_function_type IS NOT NULL
    RETURN DISTINCT s.service_function_type
    """
    results, _ = db.cypher_query(query)
    return [r[0] for r in results if r[0]]

def standardize_service_function_types():
    types = get_distinct_service_function_types()
    print(f"🔍 Found {len(types)} distinct service_function_type values.\n")

    for service_type in types:
        try:
            # Create or get CanonicalService node
            canonical = CanonicalService.nodes.get_or_none(name=service_type)
            if not canonical:
                canonical = CanonicalService(name=service_type).save()
                print(f"✅ Created CanonicalService: {service_type}")
            else:
                print(f"↪️ CanonicalService already exists: {service_type}")

            # Link matching Service nodes
            services = Service.nodes.filter(service_function_type=service_type)
            for s in services:
                if not s.is_canonical_service.is_connected(canonical):
                    s.is_canonical_service.connect(canonical)
                    print(f"🔗 Linked Service {s.uid} → CanonicalService '{service_type}'")

        except Exception as e:
            print(f"❌ Failed to process '{service_type}': {e}")

    print("\n🏁 Canonical service mapping complete.")

if __name__ == "__main__":
    standardize_service_function_types()
