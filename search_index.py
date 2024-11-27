import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import joblib

# Function to generate n-grams
def generate_ngrams(string, n=3):
    return [string[i:i+n] for i in range(len(string)-n+1)]

# Load the saved index, vectorizer, and data
index = faiss.read_index("faiss_index.bin")
vectorizer = joblib.load("vectorizer.pkl")
df = pd.read_csv("data.csv")  # Load the original CSV file

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
