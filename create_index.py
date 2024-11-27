import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import joblib

# Function to generate n-grams
def generate_ngrams(string, n=3):
    return [string[i:i+n] for i in range(len(string)-n+1)]

# Load data into a DataFrame
data = {
    'dimension_name': ['dim1', 'dim2', 'dim3', 'dim4', 'dim5', 'dim6'],
    'value': ['Michael', 'Michelle', 'Mikaela', 'Mike', 'Miguel', 'Mikhail']
}
df = pd.DataFrame(data)

# Preprocess the data
corpus = [" ".join(generate_ngrams(value.lower())) for value in df['value']]

# Create TF-IDF vectorizer and compute embeddings
vectorizer = TfidfVectorizer(analyzer='word')
tfidf_matrix = vectorizer.fit_transform(corpus).toarray()

# Create FAISS index
d = tfidf_matrix.shape[1]  # Dimension of the TF-IDF vector
index = faiss.IndexFlatL2(d)  # L2 distance for similarity search
index.add(tfidf_matrix.astype('float32'))  # Add embeddings to FAISS index

# Save the index and vectorizer
faiss.write_index(index, "faiss_index.bin")
joblib.dump(vectorizer, "vectorizer.pkl")
df.to_csv("data.csv", index=False)

print("Index and vectorizer saved successfully.")
