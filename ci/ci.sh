#!/usr/bin/env bash

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
NO_COLOR="\033[0m"

PYTHON='python3.11'

init () {
    export POSTGRES_HOST=localhost
    export POSTGRES_PORT=5432
    export POSTGRES_USER=local
    export POSTGRES_PASSWORD=local
    export POSTGRES_DB=local
}
check_pep8 () {
    if [[ -z ${1} ]]; then
        printf "${BLUE}Please input LOCATION for checking.${NO_COLOR}\n";
        return 0
    fi
    printf "${GREEN}Checking PEP8 convention in ${1}...\n"
    printf '%.0s-' $(seq 1 50)
    printf "${NO_COLOR}\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}
run_unit_tests () {
    if [[ -z ${1} ]]; then
        printf "${BLUE}Please input LOCATION for testing.${NO_COLOR}\n";
        return 0
    fi
    printf "${GREEN}Running unit tests in ${1}...\n"
    printf '%.0s-' $(seq 1 50)
    printf "${NO_COLOR}\n"
    ${PYTHON} -m pytest ${1} \
        --disable-warnings \
        -vv \
        --cov ${1} \
        --cov-report term-missing \
        --cov-fail-under=100
    if [ $? != 0 ]; then
        exit 1
    fi
}

# Execute function
$*
