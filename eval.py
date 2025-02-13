import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DB_PATH = "quotes.db"

# --- Helper functions to create tables ---
def create_generated_quotes_table(db_path=DB_PATH):
    print("[INFO] Creating 'generated_quotes' table if it doesn't exist...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS generated_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file TEXT,
            theme TEXT,
            "order" INTEGER,
            Speaker TEXT,
            Quote TEXT,
            Relevance TEXT,
            Reasoning TEXT,
            eval INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("[INFO] 'generated_quotes' table ready.")

def create_comparison_results_table(db_path=DB_PATH):
    print("[INFO] Creating 'comparison_results' table if it doesn't exist...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comparison_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file TEXT,
            theme TEXT,
            "order" INTEGER,
            Speaker TEXT,
            Quote TEXT,
            Relevance TEXT,
            Reasoning TEXT,
            eval_match REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("[INFO] 'comparison_results' table ready.")

def create_evaluation_results_table(db_path=DB_PATH):
    print("[INFO] Creating 'evaluation_results' table if it doesn't exist...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS evaluation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file TEXT,
            theme TEXT,
            prompts TEXT,
            precision REAL,
            recall REAL,
            eval_threshold REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("[INFO] 'evaluation_results' table ready.")

# --- Function 1: Save the generated_quotes JSON into SQLite ---
def save_generated_quotes(generated_quotes, db_path=DB_PATH):
    print("[INFO] Saving generated quotes to database...")
    create_generated_quotes_table(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    file_val = generated_quotes.get("file")
    theme_val = generated_quotes.get("theme")
    quotes_list = generated_quotes.get("quotes", [])
    
    for i, quote in enumerate(quotes_list, start=1):
        speaker = quote.get("Speaker")
        quote_text = quote.get("Quote")
        relevance = quote.get("Relevance")
        reasoning = quote.get("Reasoning")
        print(f"[DEBUG] Inserting quote order {i}: {quote_text[:50]}...")
        c.execute('''
            INSERT INTO generated_quotes (file, theme, "order", Speaker, Quote, Relevance, Reasoning, eval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (file_val, theme_val, i, speaker, quote_text, relevance, reasoning, 0))
    
    conn.commit()
    conn.close()
    print("[INFO] Generated quotes have been saved.")

# --- Function 2: Compare quotes using Sentence Transformers (without torch) ---
def compare_quotes(file, theme, match_threshold=95, db_path=DB_PATH):
    print(f"[INFO] Starting comparison for file: '{file}', theme: '{theme}'...")
    create_comparison_results_table(db_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print("[DEBUG] Retrieving generated quotes from DB...")
    c.execute('''
        SELECT "order", Speaker, Quote, Relevance, Reasoning FROM generated_quotes
        WHERE file = ? AND theme = ?
    ''', (file, theme))
    generated_rows = c.fetchall()
    
    print("[DEBUG] Retrieving expected quotes (eval=1) from DB...")
    c.execute('''
        SELECT Quote FROM generated_quotes
        WHERE file = ? AND theme = ? AND eval = 1
    ''', (file, theme))
    expected_rows = c.fetchall()
    conn.close()

    if not expected_rows:
        print(f"[WARN] No expected quotes (eval=1) found for file '{file}' and theme '{theme}'. Exiting comparison.")
        return

    # Extract the text for computing embeddings
    generated_quotes_text = [row[2] for row in generated_rows]  # Quote is the 3rd column
    expected_quotes_text = [row[0] for row in expected_rows]

    print("[INFO] Loading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("[INFO] Generating embeddings for generated quotes...")
    generated_embeddings = model.encode(generated_quotes_text, convert_to_tensor=False)
    
    print("[INFO] Generating embeddings for expected quotes...")
    expected_embeddings = model.encode(expected_quotes_text, convert_to_tensor=False)

    print("[INFO] Computing cosine similarities using sklearn...")
    # Compute cosine similarity between each generated quote and each expected quote.
    # This returns a 2D array of shape (num_generated, num_expected)
    cosine_scores = cosine_similarity(generated_embeddings, expected_embeddings)
    
    # For each generated quote, get the highest similarity score
    max_similarities = np.max(cosine_scores, axis=1)  # array of shape (num_generated,)
    max_similarities_percentage = (max_similarities * 100).tolist()

    print("[INFO] Saving comparison results to DB...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for row, eval_match in zip(generated_rows, max_similarities_percentage):
        order_val, speaker, quote_text, relevance, reasoning = row
        print(f"[DEBUG] Order {order_val} - Highest similarity: {eval_match:.2f}")
        c.execute('''
            INSERT INTO comparison_results (file, theme, "order", Speaker, Quote, Relevance, Reasoning, eval_match)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (file, theme, order_val, speaker, quote_text, relevance, reasoning, eval_match))
    conn.commit()
    conn.close()
    print("[INFO] Comparison complete.")

# --- Function 3: Compute precision and recall and save the evaluation result ---
def evaluate_results(file, theme, prompts, match_threshold=95, db_path=DB_PATH):
    print(f"[INFO] Starting evaluation for file: '{file}', theme: '{theme}' with threshold {match_threshold}...")
    create_evaluation_results_table(db_path)
    
    # --- Compute precision ---
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print("[DEBUG] Retrieving comparison results for precision calculation...")
    c.execute('''
        SELECT eval_match FROM comparison_results
        WHERE file = ? AND theme = ?
    ''', (file, theme))
    comp_rows = c.fetchall()
    conn.close()

    if not comp_rows:
        print(f"[WARN] No comparison results found for file '{file}' and theme '{theme}'. Exiting evaluation.")
        return None

    total_generated = len(comp_rows)
    count_generated_above_threshold = sum(1 for (score,) in comp_rows if score >= match_threshold)
    precision = (count_generated_above_threshold / total_generated) * 100
    print(f"[INFO] Precision calculated: {precision:.2f}%")

    # --- Compute recall ---
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print("[DEBUG] Retrieving expected quotes for recall calculation...")
    c.execute('''
        SELECT Quote FROM generated_quotes
        WHERE file = ? AND theme = ? AND eval = 1
    ''', (file, theme))
    expected_rows = c.fetchall()
    c.execute('''
        SELECT Quote FROM generated_quotes
        WHERE file = ? AND theme = ?
    ''', (file, theme))
    generated_rows = c.fetchall()
    conn.close()

    if not expected_rows:
        print(f"[WARN] No expected quotes (eval=1) found for file '{file}' and theme '{theme}'. Setting recall to 0.")
        recall = 0.0
    else:
        expected_quotes_text = [row[0] for row in expected_rows]
        generated_quotes_text = [row[0] for row in generated_rows]

        print("[INFO] Reloading model for recall evaluation...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("[INFO] Generating embeddings for expected quotes (recall)...")
        expected_embeddings = model.encode(expected_quotes_text, convert_to_tensor=False)
        print("[INFO] Generating embeddings for all generated quotes (recall)...")
        generated_embeddings = model.encode(generated_quotes_text, convert_to_tensor=False)
        
        print("[INFO] Computing cosine similarities for recall using sklearn...")
        cosine_scores = cosine_similarity(expected_embeddings, generated_embeddings)
        max_similarities_expected = np.max(cosine_scores, axis=1)
        max_similarities_expected_percentage = (max_similarities_expected * 100).tolist()
        count_expected_matched = sum(1 for score in max_similarities_expected_percentage if score >= match_threshold)
        total_expected = len(expected_quotes_text)
        recall = (count_expected_matched / total_expected) * 100
        print(f"[INFO] Recall calculated: {recall:.2f}%")

    result = {
        "file": file,
        "theme": theme,
        "prompts": prompts,
        "precision": precision,
        "recall": recall
    }

    print("[INFO] Saving evaluation results to database...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO evaluation_results (file, theme, prompts, precision, recall, eval_threshold)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (file, theme, json.dumps(prompts), precision, recall, match_threshold))
    conn.commit()
    conn.close()

    print("[INFO] Evaluation complete.")
    return result

# --- Example usage ---
if __name__ == "__main__":
    print("[INFO] Starting the script...")

    # Sample JSON object (generated_quotes)
    sample_json = {
        "file": "file_name.pdf",
        "theme": "nii",
        "prompts": ["junior_v2.txt", "summary_v2.txt"],
        "quotes": [
            { "Speaker": "Speaker 1", "Quote": "The quote 1", "Relevance": "0.8", "Reasoning": "Good match" },
            { "Speaker": "Speaker 2", "Quote": "The quote 2", "Relevance": "0.6", "Reasoning": "Average match" },
            { "Speaker": "Speaker 3", "Quote": "The quote 3", "Relevance": "0.9", "Reasoning": "Excellent match" },
            { "Speaker": "Speaker 4", "Quote": "The quote 4", "Relevance": "0.5", "Reasoning": "Poor match" },
            { "Speaker": "Speaker 5", "Quote": "The quote 5", "Relevance": "0.7", "Reasoning": "Good enough" }
        ]
    }

    # Save the generated quotes into the DB.
    save_generated_quotes(sample_json)

    # For demonstration, manually mark some quotes as expected ones (set eval = 1).
    print("[INFO] Marking some quotes as expected (eval=1)...")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE generated_quotes
        SET eval = 1
        WHERE "order" IN (1, 3) AND file = ? AND theme = ?
    ''', (sample_json["file"], sample_json["theme"]))
    conn.commit()
    conn.close()
    print("[INFO] Expected quotes marked.")

    # Compare the generated quotes to the expected ones.
    compare_quotes(sample_json["file"], sample_json["theme"], match_threshold=95)

    # Compute precision and recall. The eval_match threshold is configurable (default here is 95).
    evaluation = evaluate_results(sample_json["file"], sample_json["theme"], sample_json["prompts"], match_threshold=95)
    print("[RESULT] Evaluation Result:")
    print(json.dumps(evaluation, indent=4))
    print("[INFO] Script finished.")
