# config.py

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def load_private_key(private_key_env_var, passphrase_env_var=None):
    """
    Loads a private key from environment variables.
    private_key_env_var: Name of the environment variable holding the PEM text.
    passphrase_env_var: Name of the environment variable holding the passphrase (optional).
    """
    # Retrieve raw PEM text from the environment
    private_key_pem = os.environ[private_key_env_var]
    
    # Retrieve passphrase if provided (or use empty string)
    passphrase = ""
    if passphrase_env_var and passphrase_env_var in os.environ:
        passphrase = os.environ[passphrase_env_var]
    
    # Load the private key using the cryptography library
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=passphrase.encode() if passphrase else None,
        backend=default_backend()
    )
    return private_key


# Dictionary of configurations for different “areas” or “accounts”.
# Each entry holds everything needed to connect to that environment.
SNOWFLAKE_CONFIGS = {
    "SACCR": {
        "user": "SACCR_USER",         # or from env, e.g. os.getenv("SACCR_USER")
        "account": "SACCR_ACCOUNT",   # e.g. "abc12345.us-east-1"
        "warehouse": "SACCR_WH",      # optional
        "database": "SACCR_DB",       # optional
        "schema": "SACCR_SCHEMA",     # optional
        "role": "SACCR_ROLE",         # optional
        
        # We load the key from environment variables. Adjust as needed.
        "private_key": load_private_key(
            private_key_env_var="SACCR_PRIVATE_KEY",
            passphrase_env_var="SACCR_PRIVATE_KEY_PASSPHRASE"
        ),
        
        # For convenience, track which .sql file this area uses.
        "sql_file": "saccr_query.sql"
    },
    "WEALTH": {
        "user": "WEALTH_USER",
        "account": "WEALTH_ACCOUNT",
        # etc...
        
        "private_key": load_private_key(
            private_key_env_var="WEALTH_PRIVATE_KEY",
            passphrase_env_var="WEALTH_PRIVATE_KEY_PASSPHRASE"
        ),
        
        "sql_file": "wealth_query.sql"
    },
    # Add more “areas” as needed
}










# run_query.py

import sys
import snowflake.connector
from config import SNOWFLAKE_CONFIGS

def run_snowflake_query(area_name):
    """
    area_name: e.g. 'SACCR' or 'WEALTH'
    """
    # Grab the dictionary for the requested area
    cfg = SNOWFLAKE_CONFIGS.get(area_name)
    if cfg is None:
        raise ValueError(f"Area '{area_name}' not found in SNOWFLAKE_CONFIGS.")

    # The 'sql_file' is whichever SQL script we want to run for that area.
    sql_file = cfg.get("sql_file", "")
    if not sql_file:
        raise ValueError(f"No SQL file specified for area '{area_name}'.")

    # Connect using unpacked credentials (including private_key).
    conn = snowflake.connector.connect(**cfg)
    
    try:
        cursor = conn.cursor()
        
        with open(sql_file, "r") as f:
            sql_script = f.read()
        
        # Execute the SQL script
        cursor.execute(sql_script)
        
        # For a SELECT, fetch and print results
        results = cursor.fetchall()
        for row in results:
            print(row)
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # You might take the area from the command line, or default to one.
    if len(sys.argv) < 2:
        print("Usage: python run_query.py <AREA_NAME>")
        sys.exit(1)
    
    area = sys.argv[1]  # e.g. "SACCR" or "WEALTH"
    run_snowflake_query(area)
