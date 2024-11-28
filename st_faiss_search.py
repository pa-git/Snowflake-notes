# Load FAISS index and metadata
faiss_index = faiss.read_index("faiss_index.bin")
metadata = pd.read_csv("metadata.csv")

# Step 1: Generate embedding for the query
query = "Micheal"  # Example query
query_embedding = model.encode([query])

# Step 2: Search for nearest neighbors
top_k = 3  # Number of nearest neighbors
distances, indices = faiss_index.search(np.array(query_embedding, dtype='float32'), top_k)

# Step 3: Display results
for idx, dist in zip(indices[0], distances[0]):
    print(f"Dimension: {metadata.iloc[idx]['dimension_name']}, Value: {metadata.iloc[idx]['value']}, Distance: {dist:.4f}")
