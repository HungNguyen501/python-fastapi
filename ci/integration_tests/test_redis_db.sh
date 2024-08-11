#!/usr/bin/env bash

test_remove_all_keys () {
    redis-cli FLUSHDB && echo "Redis: count keys=$(redis-cli DBSIZE)";
}

# Execute function
$*
