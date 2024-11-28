import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

# Load data
csv_file = "data.csv"
df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows.")

# Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = np.array(model.encode(df['value'].tolist()), dtype='float32')

# Create and train IndexIVF
embedding_dim = embeddings.shape[1]
nlist = 500  # Number of clusters
quantizer = faiss.IndexFlatL2(embedding_dim)
index_ivf = faiss.IndexIVFFlat(quantizer, embedding_dim, nlist, faiss.METRIC_L2)
index_ivf.train(embeddings)
index_ivf.add(embeddings)
print(f"FAISS index created with {index_ivf.ntotal} entries.")

# Save the index
faiss.write_index(index_ivf, "index_ivf.bin")

# Query the index
index_ivf = faiss.read_index("index_ivf.bin")
index_ivf.nprobe = 10  # Clusters to probe

query = "fixed income"
query_embedding = np.array([model.encode(query)], dtype='float32')
distances, indices = index_ivf.search(query_embedding, 5)

for idx, dist in zip(indices[0], distances[0]):
    print(f"Category: {df.iloc[idx]['value']}, Dimension: {df.iloc[idx]['dimension_name']}, Distance: {dist:.4f}")
