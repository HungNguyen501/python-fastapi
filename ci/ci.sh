#!/usr/bin/env bash

PYTHON='python3.12'

install () {
    ${PYTHON} --version
	${PYTHON} -m pip install --upgrade pip --break-system-packages
	${PYTHON} -m pip install -r ./ci/requirements.txt --break-system-packages
}
check_pep8 () {
    if [[ -z ${1} ]]; then
        printf "Please input \"LOCATION\" for checking.\n";
        return 0
    fi
    printf "Checking PEP8 convention in ${1}...\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
}
run_unit_tests () {
    if [[ -z ${1} ]]; then
        printf "Please input \"LOCATION\" for testing.\n";
        return 0
    fi
    ${PYTHON} -m pytest ${1} \
        --disable-warnings \
        -vv \
        --cov ${1} \
        --cov-report term-missing \
        --cov-fail-under=100
}
run_integration_tests () {
    # set -e
    bash ./ci/integration_tests/test_database.sh test_connection
    bash ./ci/integration_tests/test_database.sh test_tables_deletion
    bash ./ci/integration_tests/test_database.sh test_tables_creation
    bash ./ci/integration_tests/test_user_api.sh
    bash ./ci/integration_tests/test_database.sh test_tables_deletion
}
verify_changes () {
    if [[ -z ${1} ]]; then
        printf "Input\"CHANGES\" is empty.\n";
        return 0
    fi
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "${file_name}" 2>/dev/null) ")
    done
    modules=$(bazel query --noshow_progress --output package "set(${files[*]})" 2>/dev/null)
    if [[ ! -z ${modules} ]]; then
        # Install libs
        install
        set -e
        # Check convention
        check_pep8 ${modules}
        # Run unit tests
        tests=$(bazel query --keep_going --noshow_progress --output package  "kind(test, rdeps(//..., set(${files[*]})))" 2>/dev/null)
        if [[ ! -z ${tests} ]]; then
            for test in ${tests[@]}; do
                run_unit_tests ${test}
            done
        else
            printf "No tests found\n";
        fi
    else
        printf "Changes take no effect\n";
    fi
}

# Execute function
$*
