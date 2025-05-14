#!/bin/bash
neo4j stop
timestamp=$(date +%Y%m%d_%H%M%S)
cp -r /var/lib/neo4j/data/databases/neo4j /backups/neo4j_backup_$timestamp
neo4j start
