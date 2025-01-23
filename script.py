import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def generate_embeddings(df, model_location, column="value"):
    """
    Generate embeddings for the specified column of a DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        model_location (str): Path to the SentenceTransformer model.
        column (str): Column to generate embeddings for.

    Returns:
        np.ndarray: Array of embeddings.
    """
    model = SentenceTransformer(model_location)
    return model.encode(df[column].tolist())

def create_faiss_index(embeddings):
    """
    Create a FAISS index from embeddings.
    
    Args:
        embeddings (np.ndarray): Embeddings to add to the index.

    Returns:
        faiss.IndexFlatL2: FAISS index.
    """
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(embeddings, dtype='float32'))
    return index

def save_faiss_index(index, filepath):
    """
    Save a FAISS index to a file.
    
    Args:
        index (faiss.IndexFlatL2): The FAISS index to save.
        filepath (str): Path to save the index.
    """
    faiss.write_index(index, filepath)







---------------------------------





import os
from create_index.utils import generate_embeddings, create_faiss_index, save_faiss_index
from process_jsonl.process_jsonl import process_jsonl_files

def main():
    """
    Main function to process JSONL files and create a FAISS index.
    """
    area = "Management Reporting"  # Change as needed
    model_location = "/v/region/na/appl/it/itgetl/data/dev/auto_generate_catalog/sentence-transformers/msmarco-MiniLM-L6-cos-v5"

    # Process JSONL files to get the DataFrame
    df = process_jsonl_files(area)

    # Generate embeddings from the DataFrame
    embeddings = generate_embeddings(df, model_location, column="Value")

    # Create a FAISS index using the embeddings
    faiss_index = create_faiss_index(embeddings)

    # Save the FAISS index to a file
    save_faiss_index(faiss_index, "faiss_index.bin")
    print("FAISS index and metadata saved successfully.")

if __name__ == "__main__":
    main()


