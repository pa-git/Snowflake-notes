import csv
import math

# --- Parameters ---
THRESHOLD = 0.2
INPUT_CSV = "input.csv"
OUTPUT_CSV = "output.csv"

# --- External embedding logic (assumed to be implemented) ---
def get_embedding(text):
    """
    Returns an embedding vector (list of floats) for the given text.
    Assumes the OpenAI API or other embedding logic is implemented inside here.
    """
    # Example stub (replace this):
    return [0.0] * 1536  # <- dummy vector (replace with real embedding)

# --- Stub: your answer generation logic ---
def get_answer(question):
    return "Echo: " + question

# --- Cosine distance ---
def cosine_distance(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 1.0
    return 1 - dot / (norm1 * norm2)

# --- Main process ---
def process_csv(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as infile, \
         open(output_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ['question', 'expected_answer', 'type', 'answer_received', 'match']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            question = row['question'].strip()
            expected = row['expected_answer'].strip()
            match_type = row['type'].strip().lower()

            answer = get_answer(question)
            match = "no"

            try:
                if match_type == "same":
                    if answer.strip() == expected:
                        match = "yes"
                elif match_type == "fuzzy":
                    vec1 = get_embedding(answer)
                    vec2 = get_embedding(expected)
                    distance = cosine_distance(vec1, vec2)
                    if distance <= THRESHOLD:
                        match = "yes"
                else:
                    print(f"Warning: Unknown type '{match_type}'")
            except Exception as e:
                answer = f"ERROR: {e}"
                match = "no"

            writer.writerow({
                'question': question,
                'expected_answer': expected,
                'type': match_type,
                'answer_received': answer,
                'match': match
            })

    print(f"Results written to: {output_path}")

# --- Run ---
if __name__ == "__main__":
    process_csv(INPUT_CSV, OUTPUT_CSV)
