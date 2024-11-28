import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load data into a DataFrame
data = {
    'dimension_name': ['dim1', 'dim2', 'dim3', 'dim4', 'dim5'],
    'value': ['Michael', 'Michelle', 'Mikaela', 'Mike', 'Miguel']
}
df = pd.DataFrame(data)

# Step 1: Load the Sentence Transformer model
model_name = "all-MiniLM-L6-v2"  # Choose an appropriate pre-trained model
model = SentenceTransformer(model_name)

# Step 2: Generate embeddings for the "value" column
embeddings = model.encode(df['value'].tolist())

# Step 3: Create a FAISS index
embedding_dim = embeddings.shape[1]  # Dimensionality of embeddings
faiss_index = faiss.IndexFlatL2(embedding_dim)  # Use L2 distance for similarity

# Step 4: Add embeddings to the FAISS index
faiss_index.add(np.array(embeddings, dtype='float32'))

# Optional: Store metadata (dimension_name and value)
metadata = df.reset_index(drop=True)  # Save the DataFrame to align with FAISS indices

# Save FAISS index and metadata for later use
faiss.write_index(faiss_index, "faiss_index.bin")
metadata.to_csv("metadata.csv", index=False)

print("FAISS index and metadata saved successfully.")
