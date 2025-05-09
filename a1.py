from load_contracts_neo4j import load_all_contracts_from_directory

if __name__ == "__main__":
    base_dir = "json/"  # Path to your contracts folder
    print("Starting batch load of all contracts...\n")
    load_all_contracts_from_directory(base_dir)
    print("\nAll contracts processed.")
