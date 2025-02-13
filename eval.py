import sqlite3
import json
from sentence_transformers import SentenceTransformer, util
import torch

DB_PATH = "quotes.db"


# --- Helper functions to create tables ---
def create_generated_quotes_table(db_path=DB_PATH):
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


def create_comparison_results_table(db_path=DB_PATH):
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


def create_evaluation_results_table(db_path=DB_PATH):
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


# --- Function 1: Save the generated_quotes JSON into SQLite ---
def save_generated_quotes(generated_quotes, db_path=DB_PATH):
    """
    Saves the JSON object into the `generated_quotes` table.
    The JSON object is expected to have keys: file, theme, prompts, quotes.
    Each quote is saved with its order (starting at 1) and an eval defaulting to 0.
    """
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
        # Insert each quote with eval defaulting to 0
        c.execute('''
            INSERT INTO generated_quotes (file, theme, "order", Speaker, Quote, Relevance, Reasoning, eval)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (file_val, theme_val, i, speaker, quote_text, relevance, reasoning, 0))
    
    conn.commit()
    conn.close()


# --- Function 2: Compare quotes using Sentence Transformers ---
def compare_quotes(file, theme, match_threshold=95, db_path=DB_PATH):
    """
    For the given file and theme, this function:
      1. Retrieves the generated quotes (all rows) and the expected quotes (rows with eval = 1)
      2. Computes cosine similarity between each generated quote and all expected quotes.
      3. For each generated quote, saves the highest similarity (multiplied by 100) as eval_match.
         (A perfect match would give eval_match=100.)
      4. Saves the results into the `comparison_results` table.
    
    The parameter match_threshold is not used in the computation here but can be later used to compute
    precision and recall.
    """
    create_comparison_results_table(db_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Retrieve all generated quotes for the file and theme
    c.execute('''
        SELECT "order", Speaker, Quote, Relevance, Reasoning FROM generated_quotes
        WHERE file = ? AND theme = ?
    ''', (file, theme))
    generated_rows = c.fetchall()
    
    # Retrieve expected quotes (eval=1)
    c.execute('''
        SELECT Quote FROM generated_quotes
        WHERE file = ? AND theme = ? AND eval = 1
    ''', (file, theme))
    expected_rows = c.fetchall()
    conn.close()

    if not expected_rows:
        print(f"[compare_quotes] No expected quotes (eval=1) found for file '{file}' and theme '{theme}'.")
        return

    # Extract just the text for computing embeddings
    generated_quotes_text = [row[2] for row in generated_rows]  # Quote is the 3rd column
    expected_quotes_text = [row[0] for row in expected_rows]

    # Load the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    generated_embeddings = model.encode(generated_quotes_text, convert_to_tensor=True)
    expected_embeddings = model.encode(expected_quotes_text, convert_to_tensor=True)

    # Compute cosine similarities between each generated quote and each expected quote
    cosine_scores = util.cos_sim(generated_embeddings, expected_embeddings)
    # For each generated quote, get the highest similarity score
    max_similarities = torch.max(cosine_scores, dim=1).values  # tensor of shape (num_generated,)
    # Convert to percentage (0-100)
    max_similarities_percentage = (max_similarities * 100).tolist()

    # Save each generated quote with its eval_match into the comparison_results table
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for row, eval_match in zip(generated_rows, max_similarities_percentage):
        order_val, speaker, quote_text, relevance, reasoning = row
        c.execute('''
            INSERT INTO comparison_results (file, theme, "order", Speaker, Quote, Relevance, Reasoning, eval_match)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (file, theme, order_val, speaker, quote_text, relevance, reasoning, eval_match))
    conn.commit()
    conn.close()


# --- Function 3: Compute precision and recall and save the evaluation result ---
def evaluate_results(file, theme, prompts, match_threshold=95, db_path=DB_PATH):
    """
    Computes precision and recall for the given file and theme using the following logic:
      - Precision: Percentage of generated quotes (from comparison_results)
                   that have an eval_match above the given match_threshold.
      - Recall: For each expected quote (rows with eval=1 in generated_quotes),
                compute its highest similarity (against all generated quotes).
                Recall is the percentage of expected quotes with a match above the threshold.
                
    The result is saved in the evaluation_results table and also returned as a JSON object.
    The prompts (a list) are included in the output JSON.
    """
    create_evaluation_results_table(db_path)
    
    # --- Compute precision ---
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT eval_match FROM comparison_results
        WHERE file = ? AND theme = ?
    ''', (file, theme))
    comp_rows = c.fetchall()
    conn.close()

    if not comp_rows:
        print(f"[evaluate_results] No comparison results found for file '{file}' and theme '{theme}'.")
        return None

    total_generated = len(comp_rows)
    count_generated_above_threshold = sum(1 for (score,) in comp_rows if score >= match_threshold)
    precision = (count_generated_above_threshold / total_generated) * 100

    # --- Compute recall ---
    # Get expected quotes (eval=1) and all generated quotes (their text)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
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
        print(f"[evaluate_results] No expected quotes (eval=1) found for file '{file}' and theme '{theme}'.")
        recall = 0.0
    else:
        expected_quotes_text = [row[0] for row in expected_rows]
        generated_quotes_text = [row[0] for row in generated_rows]

        # Re-load the model and compute embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')
        expected_embeddings = model.encode(expected_quotes_text, convert_to_tensor=True)
        generated_embeddings = model.encode(generated_quotes_text, convert_to_tensor=True)
        # Compute cosine similarity between each expected quote and each generated quote
        cosine_scores = util.cos_sim(expected_embeddings, generated_embeddings)
        # For each expected quote, find the maximum similarity across all generated quotes
        max_similarities_expected = torch.max(cosine_scores, dim=1).values
        max_similarities_expected_percentage = (max_similarities_expected * 100).tolist()
        count_expected_matched = sum(1 for score in max_similarities_expected_percentage if score >= match_threshold)
        total_expected = len(expected_quotes_text)
        recall = (count_expected_matched / total_expected) * 100

    # Build the evaluation result JSON
    result = {
        "file": file,
        "theme": theme,
        "prompts": prompts,
        "precision": precision,
        "recall": recall
    }

    # Save the result to the evaluation_results table
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT INTO evaluation_results (file, theme, prompts, precision, recall, eval_threshold)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (file, theme, json.dumps(prompts), precision, recall, match_threshold))
    conn.commit()
    conn.close()

    return result


# --- Example usage ---
if __name__ == "__main__":
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

    # For demonstration, let’s manually mark some quotes as the expected ones (set eval = 1).
    # For example, set eval = 1 for quotes 1 and 3.
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE generated_quotes
        SET eval = 1
        WHERE "order" IN (1, 3) AND file = ? AND theme = ?
    ''', (sample_json["file"], sample_json["theme"]))
    conn.commit()
    conn.close()

    # Compare the generated quotes to the expected ones.
    compare_quotes(sample_json["file"], sample_json["theme"], match_threshold=95)

    # Compute precision and recall. The eval_match threshold is configurable (default here is 95).
    evaluation = evaluate_results(sample_json["file"], sample_json["theme"], sample_json["prompts"], match_threshold=95)
    print("Evaluation Result:")
    print(json.dumps(evaluation, indent=4))
