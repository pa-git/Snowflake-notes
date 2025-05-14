#!/bin/bash

# --- CONFIGURATION ---
NEO4J_HOME="/var/lib/neo4j"                          # Update to your Neo4j install path
DB_NAME="neo4j"                                      # Default database name
BACKUP_DIR="/var/backups/neo4j"                      # Where to store the backups
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DEST="$BACKUP_DIR/${DB_NAME}_backup_$TIMESTAMP"

# --- STOP NEO4J ---
echo "Stopping Neo4j..."
sudo ${NEO4J_HOME}/bin/neo4j stop

# --- CREATE BACKUP DIRECTORY ---
echo "Creating backup directory at $DEST..."
mkdir -p "$DEST"

# --- COPY DATABASE FILES ---
echo "Backing up database files..."
sudo cp -r ${NEO4J_HOME}/data/databases/$DB_NAME "$DEST/"
sudo cp -r ${NEO4J_HOME}/data/transactions/$DB_NAME "$DEST/"

# --- OPTIONAL: BACKUP CONFIG (uncomment if needed) ---
# echo "Backing up configuration..."
# sudo cp -r ${NEO4J_HOME}/conf "$DEST/conf"

# --- START NEO4J ---
echo "Restarting Neo4j..."
sudo ${NEO4J_HOME}/bin/neo4j start

# --- DONE ---
echo "Backup completed successfully to $DEST"
