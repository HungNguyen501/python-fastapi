#!/usr/bin/env bash

API_URI="http://0.0.0.0:8009/api/v1"

call_user_get () {
    curl --connect-timeout 5 --location "${API_URI}/user?uuid=${1}" 2>/dev/null
}

call_user_list () {
    curl --location "${API_URI}/user/list?start=0" 2>/dev/null
}

call_user_create () {
    curl -conmect-timeout 5 --location "${API_URI}/user" \
        --header 'Content-Type: application/json' \
        --data ${1}
}

call_user_update () {
    curl --connect-timeout 5 --location --request PUT "${API_URI}/user?uuid=accfd78c-f0dc-4683-90bb-d63de643e852" \
    --header 'Content-Type: application/json' \
    --data ${1}
}

call_user_delete () {
    curl --connect-timeout 5 --location --request DELETE "${API_URI}/user?uuid=${1}"
}

test_health_check () {
    response=$(curl --connect-timeout 5 --location "${API_URI}/health" 2>/dev/null)
    if [ "${response}" == "{\"message\":\"200 OK\"}" ]; then
        printf "API is healthy\n"
    else
        printf "API is down\n"
        exit 1
    fi
}

test_empty_user_list () {
    if [ "$(call_user_list)" != "{\"total\":0,\"count\":0,\"users\":[]}" ]; then
        printf "test_empty_user_list Failed\n"
        exit 1
    fi
}

test_user_get_with_wrong_uuid () {
    actual="{'detail':[{'type':'uuid_parsing','loc':['query','uuid'],'msg':" \
        'Input should be a valid UUID, invalid group count: expected 5, found 2'," \
        'input':'-1','ctx':{'error':'invalid group count: expected 5, found 2'}}]}"
    # if [ $(call_user_get -1) != ${actual} ]; then
    #     printf "test_user_get_with_wrong_uuid Failed\n"
    # fi
    echo $actual
}

# Execute function
$*
