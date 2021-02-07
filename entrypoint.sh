#!/bin/bash

# This script starts first after container initialization.

CACHE_DIR="/var/cache/birthday-lord-bot"
DB_FILE="$CACHE_DIR/db.db"

if [[ ! -d "$CACHE_DIR" ]]
then
    echo "Creating $CACHE_DIR..."
    mkdir -p "$CACHE_DIR"
fi

if [[ ! -f "$DB_FILE" ]]
then
    echo "Db isn't created. Creating..."
    sqlite3 "$DB_FILE" < createdb.sql
fi

echo "Launching bot"
python run.py --config config.yaml
