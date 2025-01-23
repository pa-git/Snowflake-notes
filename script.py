# config.py

BASE_DIRECTORY = "./data/"

CONFIG = {
    "Management Reporting": {
        "sub_directory": "management_reporting/",
        "jsonl_files": ["file1.jsonl", "file2.jsonl"],
        "dimension_key": "dimension_name",
        "value_keys": ["value1", "value2"]
    },
    "Sales Reporting": {
        "sub_directory": "sales_reporting/",
        "jsonl_files": ["sales_data.jsonl"],
        "dimension_key": "sales_dimension",
        "value_keys": ["amount", "currency"]
    }
}

# utils.py

import os
import jsonlines
import pandas as pd

def load_jsonl_file(filepath):
    """
    Loads a JSONL file and returns a list of JSON objects.
    """
    data = []
    with jsonlines.open(filepath) as reader:
        for obj in reader:
            data.append(obj)
    return data

def deduplicate_dataframe(df):
    """
    Deduplicates a pandas DataFrame.
    """
    return df.drop_duplicates()

# clean_and_filter.py

import os
import pandas as pd
from config import CONFIG, BASE_DIRECTORY
from utils import load_jsonl_file, deduplicate_dataframe

def process_jsonl_files(area):
    """
    Processes JSONL files for the specified business area and returns a DataFrame.

    Args:
        area (str): The business area to process (e.g., "Management Reporting").

    Returns:
        pandas.DataFrame: A DataFrame with two columns: Dimension and Value.
    """
    # Load configuration for the area
    if area not in CONFIG:
        raise ValueError(f"Area '{area}' not found in configuration.")

    area_config = CONFIG[area]
    sub_directory = area_config["sub_directory"]
    directory = os.path.join(BASE_DIRECTORY, sub_directory)
    jsonl_files = area_config["jsonl_files"]
    dimension_key = area_config["dimension_key"]
    value_keys = area_config["value_keys"]

    # Initialize an empty list to hold the processed rows
    rows = []

    # Process each file in the directory
    for jsonl_file in jsonl_files:
        filepath = os.path.join(directory, jsonl_file)

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        # Load the JSONL file
        data = load_jsonl_file(filepath)

        # Extract dimensions and values from each JSON object
        for record in data:
            dimension = record.get(dimension_key)
            if not dimension:
                continue

            for value_key in value_keys:
                value = record.get(value_key)
                if value:
                    rows.append({"Dimension": dimension, "Value": value})

    # Convert the rows to a pandas DataFrame
    df = pd.DataFrame(rows)

    # Deduplicate the DataFrame
    df = deduplicate_dataframe(df)

    return df

if __name__ == "__main__":
    # Example usage
    area = "Management Reporting"  # Change as needed
    df = process_jsonl_files(area)
    df.to_csv("output.csv", index=False)
    print("DataFrame saved as output.csv")
