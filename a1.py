#!/bin/bash

# --- CONFIGURATION ---
NEO4J_HOME="/var/lib/neo4j"          # Update this to match your Neo4j install path
DB_NAME="neo4j"                      # Default database name

# --- STOP NEO4J ---
echo "Stopping Neo4j..."
sudo ${NEO4J_HOME}/bin/neo4j stop

# --- DELETE DATABASE AND TRANSACTIONS ---
echo "Deleting database and transaction data..."
sudo rm -rf ${NEO4J_HOME}/data/databases/${DB_NAME}
sudo rm -rf ${NEO4J_HOME}/data/transactions/${DB_NAME}

# --- OPTIONAL: CLEAR LOGS (uncomment if needed) ---
# echo "Clearing logs..."
# sudo rm -rf ${NEO4J_HOME}/logs/*

# --- START NEO4J ---
echo "Starting Neo4j..."
sudo ${NEO4J_HOME}/bin/neo4j start

# --- DONE ---
echo "Neo4j hard reset complete. A fresh empty database has been initialized."
