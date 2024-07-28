#!/usr/bin/env bash

test_connection () {
    psql postgres://local:local@localhost:5432/local -c "select 1;"
    if [ $? != 0 ]; then
        printf "Connection failed\n"
        exit 1
    fi
}

test_tables_creation () {
    python3.11 -c "from src.db.database import DatabaseConnection; db = DatabaseConnection(); db.connect(); db.create_tables();";
}

# Execute function
$*
