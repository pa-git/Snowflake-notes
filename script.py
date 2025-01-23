import os

CONFIG = {
    "areas": {
        "Management Reporting": {
            "output_index_path": os.path.join("indices", "management_reporting_faiss_index.bin"),
        },
        "Sales Reporting": {
            "output_index_path": os.path.join("indices", "sales_reporting_faiss_index.bin"),
        },
    }
}

# Determine model location
if os.environ.get("IS_CONTAINER") == "Docker":
    home_dir = os.getenv("HOME")
    if not home_dir:
        raise EnvironmentError("HOME environment variable is not set.")
    CONFIG["model_location"] = os.path.normpath(
        os.path.join(home_dir, "model-store", "sentence-transformers", "msmarco-MiniLM-L6-cos-v5")
    )
else:
    CONFIG["model_location"] = "/v/region/na/appl/it/itgetl/data/dev/auto_generate_catalog/sentence-transformers/msmarco-MiniLM-L6-cos-v5"

# Log the model location for debugging
print(f"Model location set to: {CONFIG['model_location']}")
