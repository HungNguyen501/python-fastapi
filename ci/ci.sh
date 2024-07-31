#!/usr/bin/env bash

PYTHON='python3.12'

check_pep8 () {
    if [[ -z ${1} ]]; then
        printf "Please input \"LOCATION\" for checking.\n";
        return 0
    fi
    printf "Checking PEP8 convention in ${1}...\n"
    ${PYTHON} -m flake8 ${1} --show-source --statistics && ${PYTHON} -m pylint ${1}
    if [ $? != 0 ]; then
        exit 1
    fi
}
run_unit_tests () {
    if [[ -z ${1} ]]; then
        printf "Please input \"LOCATION\" for testing.\n";
        return 0
    fi
    printf "Running unit tests in ${1}...\n"
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
check_incremental_changes () {
    if [[ -z ${1} ]]; then
        printf "Input(CHANGES) is empty.\n";
        return 0
    fi
    files=()
    IFS=',' read -r -a changed_files <<< "${1}"
    for file_name in ${changed_files[@]}; do
        files+=("$(bazel query --keep_going --noshow_progress "${file_name}" 2>/dev/null) ")
    done
    modules=$(bazel query --noshow_progress --output package "set(${files[*]})" 2>/dev/null)
    if [[ ! -z ${modules} ]]; then
        make install
        check_pep8 ${modules}
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
        printf '%.0s-' $(seq 1 30);
    fi
}

# Execute function
$*
