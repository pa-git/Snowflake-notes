import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import joblib

# Function to generate n-grams
def generate_ngrams(string, n=3):
    return [string[i:i+n] for i in range(len(string)-n+1)]

# Load data from CSV file
csv_file = "data.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Preprocess the 'value' column
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

print("Index and vectorizer saved successfully.")
