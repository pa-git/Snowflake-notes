import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import faiss

# Sample dataframe
data = {
    'dimension_name': ['dim1', 'dim2', 'dim3', 'dim4', 'dim5', 'dim6'],
    'value': ['Michael', 'Michelle', 'Mikaela', 'Mike', 'Miguel', 'Mikhail']
}
df = pd.DataFrame(data)

# Generate tri-grams for the 'value' column
def generate_ngrams(string, n=3):
    return [string[i:i+n] for i in range(len(string)-n+1)]

# Preprocess the data
corpus = [" ".join(generate_ngrams(value.lower())) for value in df['value']]

# Create TF-IDF vectorizer and compute embeddings
vectorizer = TfidfVectorizer(analyzer='word')
tfidf_matrix = vectorizer.fit_transform(corpus).toarray()

# Create FAISS index
d = tfidf_matrix.shape[1]  # Dimension of the TF-IDF vector
index = faiss.IndexFlatL2(d)  # L2 distance for similarity search
index.add(tfidf_matrix.astype('float32'))  # Add embeddings to FAISS index

# Function to search for top matches
def search_faiss(query, vectorizer, index, df, top_n=5):
    # Preprocess the query into tri-grams
    query_trigrams = " ".join(generate_ngrams(query.lower()))
    query_vector = vectorizer.transform([query_trigrams]).toarray().astype('float32')
    
    # Search in FAISS index
    distances, indices = index.search(query_vector, top_n)
    
    # Collect results
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # Ignore invalid indices
            results.append({
                'value_found': df.iloc[idx]['value'],
                'distance': distances[0][i],
                'dimension_name': df.iloc[idx]['dimension_name']
            })
    
    return results

# Example query
query_name = "Micheal"
results = search_faiss(query_name, vectorizer, index, df)

# Output results
for i, res in enumerate(results, 1):
    print(f"Rank: {i}, Dimension: {res['dimension_name']}, Value: {res['value_found']}, Distance: {res['distance']:.4f}")
