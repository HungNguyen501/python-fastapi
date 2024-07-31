#!/usr/bin/env bash

export POSTGRES_HOST=127.0.0.1
export POSTGRES_PORT=5432
export POSTGRES_USER=local
export POSTGRES_PASSWORD=local
export POSTGRES_DB=local

test_connection () {
    psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB} -c "select 1 as connected;"
}

test_tables_creation () {
    python3 -c "from src.db.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.create_tables();";
}

test_tables_deletion () {
    python3 -c "from src.db.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.drop_tables();";
}

# Execute function
$*
