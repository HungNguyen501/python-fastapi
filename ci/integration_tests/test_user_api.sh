#!/usr/bin/env bash

API_URI="http://127.0.0.1:8009/api/v1"

call_health_check () {
    curl --connect-timeout 5 --retry 10 --retry-delay 3 --retry-all-errors "${API_URI}/health" 2>/dev/null
}

call_user_login () {
    curl --connect-timeout 5 --location --request POST "${API_URI}/auth" \
        --header 'accept: application/json' \
        --form 'grant_type="password"' \
        --form "username=${1}" \
        --form "password=${2}" 2>/dev/null
}

call_user_get () {
    curl --connect-timeout 5 --location --request GET "${API_URI}/user" \
        --header "Authorization: Bearer ${1}" \
        --header 'Content-Type: application/json' 2>/dev/null
}

call_user_list () {
    curl --connect-timeout 5 --location "${API_URI}/user/list?start=0&page_size=10" 2>/dev/null
}

call_user_create () {
    curl --connect-timeout 5 --location --request POST "${API_URI}/user" \
        --header 'Content-Type: application/json' \
        --data "${1}"
}

call_user_update () {
    curl --connect-timeout 5 --location --request PUT "${API_URI}/user" \
        --header "Authorization: Bearer ${1}" \
        --header 'Content-Type: application/json' \
        --data "${2}"
}

call_user_delete () {
    curl --connect-timeout 5 --location --request DELETE "${API_URI}/user" \
        --header "Authorization: Bearer ${1}" \
        --header 'Content-Type: application/json'
}

assess_results () {
    if [[ "${1}" != "${2}" ]]; then
        echo "__Failed__: actual=${1} <> expected=${2}"
        exit 1
    fi
    echo "__Passed__: actual=${1} == expected=${2}"
}

echo "⇨ Test api_health_check"
actual=$(call_health_check)
expected='{"message":"200 OK"}'
assess_results "${actual}" "${expected}"

echo "⇨ Test empty user_list"
actual=$(call_user_list)
expected="{\"total\":0,\"count\":0,\"users\":[]}"
assess_results "${actual}" "${expected}"

echo "⇨ Test create_user"
for data in '{"name": "user1", "password": "123"}' '{"name": "user2", "password": "123"}' '{"name": "user3", "password": "123"}'; do
    actual=$(call_user_create "${data}" 2>/dev/null)
    expected='{"message":"created"}'
    assess_results "${actual}" "${expected}"
done
actual=$(call_user_list | jq --raw-output ".total")
expected=3
assess_results "${actual}" "${expected}"

echo "⇨ Test user_login"
actual=$(call_user_login "user1" "123" | jq --raw-output ".token_type")
expected="bearer"
assess_results "${actual}" "${expected}"
actual=$(call_user_login "fake_name" "fake_pass")
expected='{"error":"Incorrect username or password"}'
assess_results "${actual}" "${expected}"

echo "⇨ Test update_user"
for username in $(call_user_list | jq --raw-output ".users[].name" | tail -1); do
    access_token=$(call_user_login "${username}" "123" | jq --raw-output ".access_token")
    actual=$(call_user_update ${access_token} '{"password": "456"}' 2>/dev/null)
    expected='{"message":"updated"}'
    assess_results "${actual}" "${expected}"
done
actual=$(call_user_list | jq --raw-output ".total")
expected=3
assess_results "${actual}" "${expected}"

echo "⇨ Test update_username"
access_token=$(call_user_login "$(call_user_list | jq --raw-output ".users[].name" | tail -1)" "456" | jq --raw-output ".access_token")
actual=$(call_user_update ${access_token} '{"username": "f8"}' 2>/dev/null)
expected='{"detail":[{"type":"missing","loc":["body","password"],"msg":"Field required","input":{"username":"f8"}}]}'
assess_results "${actual}" "${expected}"

echo "⇨ Test update_user failed"
access_token=$(call_user_login "$(call_user_list | jq --raw-output ".users[].name" | tail -1)" "123" | jq --raw-output ".access_token")
actual=$(call_user_update ${access_token} '{"password": "123"}' 2>/dev/null)
expected='{"error":"Invalid credentials"}'
assess_results "${actual}" "${expected}"

echo "⇨ Test delete_user"
access_token=$(call_user_login "$(call_user_list | jq --raw-output ".users[].name" | tail -1)" "456" | jq --raw-output ".access_token")
actual=$(call_user_delete ${access_token} 2>/dev/null)
expected='{"message":"deleted"}'
assess_results "${actual}" "${expected}"
# Check user_count
actual=$(call_user_list | jq --raw-output ".total")
expected=2
assess_results "${actual}" "${expected}"

echo "⇨ Test get_user"
access_token=$(call_user_login "$(call_user_list | jq --raw-output ".users[].name" | tail -1)" "123" | jq --raw-output ".access_token")
actual=$(call_user_get ${access_token} 2>/dev/null | jq --raw-output ".password")
expected='$2b$12$eeeeeeeeeeeeeeeeeeeeeedJLEz7e/.bs.BVKXsxbOT1ORiO5/EAe'
assess_results "${actual}" "${expected}"

echo "⇨ Test get_user by invalid credentials"
actual=$(call_user_get "fake_access_token" 2>/dev/null)
expected='{"error":"Invalid credentials"}'
assess_results "${actual}" "${expected}"
