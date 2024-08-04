#!/usr/bin/env bash

API_URI="http://127.0.0.1:8009/api/v1"

call_health_check () {
    curl --connect-timeout 5 --retry 10 --retry-delay 3 --retry-all-errors "${API_URI}/health" 2>/dev/null
}

call_user_get () {
    curl --connect-timeout 5 --location "${API_URI}/user?uuid=${1}" 2>/dev/null
}

call_user_list () {
    curl --location "${API_URI}/user/list?start=0&page_size=10" 2>/dev/null
}

call_user_create () {
    curl --connect-timeout 5 --location --request POST "${API_URI}/user" \
        --header 'Content-Type: application/json' \
        --data "${1}"
}

call_user_update () {
    curl --connect-timeout 5 --location --request PUT "${API_URI}/user?uuid=${1}" \
    --header 'Content-Type: application/json' \
    --data "${2}"
}

call_user_delete () {
    curl --connect-timeout 5 --location --request DELETE "${API_URI}/user?uuid=${1}"
}

assess_results () {
    if [[ "${1}" != "${2}" ]]; then
        printf "__Failed__: actual=${1} <> expected=${2}\n"
        exit 1
    fi
    printf "__Passed__: actual=${1} == expected=${2}\n"
}

printf "⇨ Test api_health_check\n"
actual=$(call_health_check)
expected='{"message":"200 OK"}'
assess_results "${actual}" "${expected}"

printf "⇨ Test empty user_list\n"
actual=$(call_user_list)
expected="{\"total\":0,\"count\":0,\"users\":[]}"
assess_results "${actual}" "${expected}"

printf "⇨ Test create_user\n"
for data in '{"name": "user1"}' '{"name": "user2"}' '{"name": "user3"}' '{"name": "user4"}' '{"name": "user5"}' '{"name": "user6"}' '{"name": "user7"}'; do
    actual=$(call_user_create "${data}" 2>/dev/null)
    expected='{"message":"created"}'
    assess_results "${actual}" "${expected}"
done
actual=$(call_user_list | jq --raw-output ".total")
expected=7
assess_results "${actual}" "${expected}"

printf "⇨ Test update_user\n"
for uuid in $(call_user_list | jq --raw-output ".users[].uuid" | tail -5); do
    actual=$(call_user_update "${uuid}" '{"name": "fake1"}' 2>/dev/null)
    expected='{"message":"updated"}'
    assess_results "${actual}" "${expected}"
done
actual=$(call_user_list | jq --raw-output ".total")
expected=7
assess_results "${actual}" "${expected}"

printf "⇨ Test update_user by wrong uuid format\n"
actual=$(call_user_update "-1" '{"name": "fake1"}' 2>/dev/null)
expected='{"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]}'
assess_results "${actual}" "${expected}"

printf "⇨ Test update_user by not found uuid\n"
actual=$(call_user_update "a00a0aaa-0aa0-00a0-00aa-0a0aa0aa00a0" '{"name": "fake1"}' 2>/dev/null)
expected='{"error":"User not found"}'
assess_results "${actual}" "${expected}"

printf "⇨ Test update_user by wrong schema\n"
uuid=$(call_user_list | jq --raw-output ".users[].uuid" | tail -1)
actual=$(call_user_update "${uuid}" '{"wrong_field_name": "fake1"}' 2>/dev/null)
expected='{"error":"null value in column \"name\" of relation \"users\" violates not-null constraint"}'
assess_results "${actual}" "${expected}"

printf "⇨ Test delete_user\n"
for uuid in $(call_user_list | jq --raw-output ".users[].uuid" | tail -5); do
    actual=$(call_user_delete "${uuid}" 2>/dev/null)
    expected='{"message":"deleted"}'
    assess_results "${actual}" "${expected}"
done
actual=$(call_user_list | jq --raw-output ".total")
expected=2
assess_results "${actual}" "${expected}"

printf "⇨ Test get_user\n"
actual=$(call_user_get $(call_user_list | jq --raw-output ".users[].uuid" | tail -1) | jq --raw-output ".name")
expected='user2'
assess_results "${actual}" "${expected}"

printf "⇨ Test get_user by wrong uuid format\n"
actual=$(call_user_get -1)
expected='{"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]}'
assess_results "${actual}" "${expected}"

printf "⇨ Test get_user by not found user\n"
actual="$(call_user_get accfd78c-f0dc-4683-90bb-d63de643e852)"
expected='{"error":"User not found"}'
assess_results "${actual}" "${expected}"
