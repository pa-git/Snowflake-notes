Below is a sample **README** you can adapt and add to your repository. Customize the sections as needed to reflect your environment, tooling, and any specific instructions or conventions.

---

# TM1 Data Extraction & FAISS Indexing

This repository provides a set of Python scripts to:
1. Extract data from **TM1** cubes (dimensions and attributes),
2. Clean and filter the extracted data,
3. Create **FAISS** indices for semantic search,
4. Perform search on the created indices.

---

## Table of Contents

1. [Overview](#overview)  
2. [Project Structure](#project-structure)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [1. Data Extraction](#1-data-extraction)  
   - [2. Data Processing](#2-data-processing)  
   - [3. Index Creation](#3-index-creation)  
   - [4. Search](#4-search)  
6. [Configuration](#configuration)  
7. [Troubleshooting](#troubleshooting)  
8. [License](#license)

---

## Overview

Many business intelligence processes involve fetching data from TM1, transforming it, and then providing the transformed data for downstream applications like semantic search. This application automates that workflow:

1. **Data Extraction**: Fetch dimension and attribute data from TM1 cubes, storing them as JSONL files.  
2. **Data Processing**: Load and clean the extracted JSONL data, producing a Pandas DataFrame.  
3. **Index Creation**: Convert the text data into embeddings using a SentenceTransformer model, and build a FAISS index for efficient similarity search.  
4. **Search**: Query the FAISS index to find nearest neighbors (semantic matches) to a given query.

---

## Project Structure

```
├── data_extraction/
│   ├── extracted_values/          # Output directory for extracted JSONL files
│   ├── __init__.py
│   ├── config.py                  # Configuration for extraction (cubes, dimensions, etc.)
│   ├── extract_values.py          # Script to connect to TM1 and extract data
│   └── utils.py                   # Helper functions for dimension processing
│
├── data_processing/
│   ├── __init__.py
│   ├── config.py                  # Configuration for data processing (files, directories)
│   ├── process_jsonl.py           # Script to load and process JSONL files into DataFrame
│   └── utils.py                   # Helper functions for data processing
│
├── index_creation/
│   ├── indices/                   # Output directory for FAISS index files
│   ├── __init__.py
│   ├── config.py                  # Configuration for index creation (model paths, output index paths)
│   ├── create_index.py            # Script to generate embeddings and create a FAISS index
│   └── utils.py                   # Helper functions (embed text, create/save FAISS index)
│
├── search/
│   ├── __init__.py
│   ├── search_index.py            # Script to perform search on a FAISS index
│   └── utils.py                   # Search-related helper functions
│
└── read_me.md                     # README with instructions (this file)
```

---

## Requirements

- **Python 3.7+** (or the version your environment supports)
- **TM1py** for connecting to TM1
- **pandas** for data manipulation
- **jsonlines** for reading/writing JSONL
- **SentenceTransformer** for generating text embeddings
- **faiss** for creating and querying FAISS indices
- (Optional) **logging** for more robust logging instead of raw `print()` statements

You can install the major dependencies with:

```bash
pip install -r requirements.txt
```

*(Note: Ensure you maintain an up-to-date `requirements.txt` or use a `pyproject.toml` if you prefer a more modern Python packaging approach.)*

---

## Installation

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/your-organization/your-repo.git
   cd your-repo
   ```
2. **Set Up Virtual Environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Below is the typical end-to-end workflow. You can also run each step independently if you only need a subset of the functionality.

### 1. Data Extraction

To extract data from TM1, edit `data_extraction/config.py` as necessary (e.g., specify the cubes and dimensions). Then run:

```bash
cd data_extraction
python extract_values.py
```

- This will connect to TM1 (using credentials or config from your environment) and write **JSONL** files to `data_extraction/extracted_values/...`.

### 2. Data Processing

To transform/clean the extracted JSONL files into a Pandas DataFrame:

```bash
cd ../data_processing
python process_jsonl.py
```

- This reads from the paths configured in `data_processing/config.py` and outputs a DataFrame as CSV (by default named `output.csv`).  
- *Note*: Ensure `sub_directory` or `directory` in the config matches the actual folder name in `extracted_values/`.

### 3. Index Creation

To create a **FAISS** index from the processed data:

```bash
cd ../index_creation
python create_index.py
```

- This script:
  1. Optionally calls the extraction script again (depending on the area)  
  2. Calls the processing script to get a fresh DataFrame  
  3. Embeds the data using a SentenceTransformer model  
  4. Creates a FAISS index and saves it to `index_creation/indices/`

- Model location is determined by environment variables or the default path in `index_creation/config.py`. Make sure the **SentenceTransformer** model is accessible at the specified path.

### 4. Search

Finally, to query the FAISS index:

```bash
cd ../search
python search_index.py
```

- This will load your saved index and the **SentenceTransformer** model, then prompt or accept a query for semantic search.  
- Make sure the script is configured to reference the same `indices/*.bin` file that was created in the **Index Creation** step.

---

## Configuration

### TM1 Connection

- The TM1 configuration references code like `finpyalpyn.server.config.ServerConfig` and `Environment.DEV` or `Instance.FINANCE`.  
- **Ensure** you have the correct credentials or environment variables to connect to TM1.  
- Update `data_extraction/extract_values.py` (and any relevant script) with the environment/instance you need:
  ```python
  if __name__ == "__main__":
      extract_tm1_data(Environment.DEV, Instance.FINANCE, 'Management Reporting')
  ```

### Model Location

- In `index_creation/config.py`, the model path is determined by `IS_CONTAINER` environment variable or a default path.  
- If you run locally, ensure you have:
  - `IS_CONTAINER` set to something other than `"Docker"`, or
  - The correct path specified in the default `model_location`.

---

## Troubleshooting

1. **Only One JSONL File Processes**  
   - Make sure you don’t have a premature `return` in the data processing script.  
   - Check for indentation issues that might break the loop.
2. **File Not Found Errors**  
   - Confirm that the `directory` and `sub_directory` keys in the configs match actual folders.  
   - Verify that your relative paths are correct if you run scripts from different working directories.
3. **No Data After Extraction**  
   - Confirm that the TM1 environment is reachable and your `CUBE_CONFIG` matches the actual cube/dimension names.
4. **FAISS Index Not Found**  
   - Double-check the `output_index_path` in `index_creation/config.py`.  
   - Ensure the index creation step completes successfully before searching.

---

## License

*(Optional: Include your project's license terms, e.g., MIT, Apache, etc.)*

---

## Contact / Contributing

- **Contact**: [Your Name] (<your.email@domain.com>)  
- Contributions via pull requests are welcome. Please submit an issue first to discuss proposed changes.

---

*End of README*
