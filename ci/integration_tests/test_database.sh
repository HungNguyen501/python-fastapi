#!/usr/bin/env bash

export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=local
export POSTGRES_PASSWORD=local
export POSTGRES_DB=local

test_connection () {
    psql postgres://local:local@localhost:5432/local -c "select 1 as connected;"
    if [ $? != 0 ]; then
        printf "Connection failed\n"
        exit 1
    fi
}

test_tables_creation () {
    python3.11 -c "from src.db.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.create_tables();";
}

test_tables_deletion () {
    python3.11 -c "from src.db.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.drop_tables();";
}

# Execute function
$*
