#!/usr/bin/env bash

PYTHON='python3'

install () {
    ${PYTHON} --version
	${PYTHON} -m pip install --upgrade pip --quiet --break-system-packages
    echo "► Installing..."
    cat ./ci/requirements.txt 
	${PYTHON} -m pip install --quiet -r ./ci/requirements.txt --break-system-packages
    echo "► Done!"
}

check_pep8 () {
    printf "Checking PEP8 convention in ${1}...\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
}

run_unit_tests () {
    ${PYTHON} -m pytest ${1} \
        --disable-warnings \
        -vv \
        --cov ${1} \
        --cov-report term-missing \
        --cov-fail-under=100
}

run_integration_tests () {
    set -e
    export POSTGRES_HOST=127.0.0.1
    export POSTGRES_PORT=5432
    export POSTGRES_USER=local
    export POSTGRES_PASSWORD=local
    export POSTGRES_DB=local
    echo "► Start integration tests..."
    bash ./ci/integration_tests/test_database.sh test_connection
    bash ./ci/integration_tests/test_database.sh test_tables_deletion
    bash ./ci/integration_tests/test_database.sh test_tables_creation
    bash ./ci/integration_tests/test_redis_db.sh test_remove_all_keys
    # bash ./ci/integration_tests/test_user_api.sh
    # bash ./ci/integration_tests/test_database.sh test_tables_deletion
    echo "► Done integration test!"
}

verify_changes () {
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "${file_name}" 2>/dev/null) ")
    done
    modules=$(bazel query --noshow_progress --output package "set(${files[*]})" 2>/dev/null)
    if [[ -z ${modules} ]]; then
        printf "Changes take no effect.\n" && exit 0
    fi
    set -e
    # Check convention
    check_pep8 ${modules}
    # Run unit tests
    tests=$(bazel query \
        --keep_going \
        --noshow_progress \
        --output package  \
        "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
    if [[ ! -z ${tests} ]]; then
        for test in ${tests[@]}; do run_unit_tests ${test}; done
    fi
}

# Execute function
$*
