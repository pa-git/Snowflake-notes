import json

def get_scenarios() -> list[dict]:
    with open("scenarios.jsonl", "r") as f:
        return [json.loads(line) for line in f if line.strip()]
