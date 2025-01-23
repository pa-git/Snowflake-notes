CONFIG = {
    "model_location": "/v/region/na/appl/it/itgetl/data/dev/auto_generate_catalog/sentence-transformers/msmarco-MiniLM-L6-cos-v5",
    "areas": {
        "Management Reporting": {
            "output_index_path": "management_reporting_faiss_index.bin"
        },
        "Sales Reporting": {
            "output_index_path": "sales_reporting_faiss_index.bin"
        }
    }
}

"output_index_path": os.path.join("indices", "management_reporting_faiss_index.bin")


import os
import numpy as np
from create_index.utils import generate_embeddings, create_faiss_index, save_faiss_index
from process_jsonl.process_jsonl import process_jsonl_files
from config import CONFIG

def main():
    """
    Main function to process multiple areas and create FAISS indices.
    """
    model_location = CONFIG["model_location"]
    areas_config = CONFIG["areas"]

    for area, settings in areas_config.items():
        print(f"Processing area: {area}")

        # Get output index path for this area
        output_index_path = settings["output_index_path"]

        # Process JSONL files to get the DataFrame
        df = process_jsonl_files(area)
        
        if df.empty:
            print(f"No data processed for area: {area}")
            continue

        # Generate embeddings from the DataFrame
        embeddings = generate_embeddings(df, model_location, column="Value")

        # Create a FAISS index using the embeddings
        faiss_index = create_faiss_index(embeddings)

        # Save the FAISS index to the area-specific file
        save_faiss_index(faiss_index, output_index_path)
        print(f"FAISS index for {area} saved to {output_index_path}")

if __name__ == "__main__":
    main()
