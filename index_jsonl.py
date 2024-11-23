import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

def process_jsonl_files(directory, collection_name, persist_directory):
    # Initialize ChromaDB client with persistence
    client = chromadb.Client(chromadb.config.Settings(persist_directory=persist_directory))
    
    # Load or create the collection
    if collection_name in client.list_collections():
        collection = client.get_collection(collection_name)
    else:
        collection = client.create_collection(collection_name)
    
    # Load the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # List all JSONL files in the directory
    jsonl_files = [f for f in os.listdir(directory) if f.endswith('.jsonl')]
    print(f"Found {len(jsonl_files)} JSONL files: {jsonl_files}")

    # Process each JSONL file
    for jsonl_file in jsonl_files:
        file_path = os.path.join(directory, jsonl_file)
        print(f"Processing file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Parse the JSON object
                record = json.loads(line.strip())
                
                # Extract the text and metadata
                text = record.get('text')  # Assume the first attribute is 'text'
                metadata = {k: v for k, v in record.items() if k != 'text'}

                # Generate embedding for the text
                embedding = model.encode([text])[0]

                # Add to the collection
                collection.add(
                    ids=[f"{jsonl_file}_{text[:20]}"],  # Create a unique ID (e.g., file name + first 20 chars of text)
                    embeddings=[embedding],
                    metadatas=[metadata],
                    documents=[text]
                )
    
    print("Data successfully added to the collection.")
    print("Persisting collection...")

# Directory containing the JSONL files
directory = "./data/jsonl_files"

# Collection name
collection_name = "my_text_collection"

# Directory to persist ChromaDB collections
persist_directory = "./chromadb_persist"

# Run the processing function
process_jsonl_files(directory, collection_name, persist_directory)
