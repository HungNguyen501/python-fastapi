#!/usr/bin/env bash

API_URI="http://127.0.0.1:8009/api/v1"

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

printf "[test_health_check] "
response=$(curl --connect-timeout 5 --location "${API_URI}/health" 2>/dev/null)
if [ "${response}" == "{\"message\":\"200 OK\"}" ]; then
    printf "...API is healthy\n"
else
    printf "...API is down\n"
    exit 1
fi

printf "[test_empty_user_list] "
if [ "$(call_user_list)" != "{\"total\":0,\"count\":0,\"users\":[]}" ]; then
    printf "...Failed\n"
    exit 1
fi
printf "...Passed\n"

printf "[test_create_user] "
for data in '{"name": "user1"}' '{"name": "user2"}' '{"name": "user3"}' '{"name": "user4"}' '{"name": "user5"}' '{"name": "user6"}' '{"name": "user7"}'; do
    if [ $(call_user_create "${data}" 2>/dev/null) != '{"message":"created"}' ]; then
        printf "...Failed\n"
        exit 1
    fi
done
count_users=$(call_user_list | jq --raw-output ".total")
if [ ${count_users} != 7 ]; then
    printf "...Failed (count_user: actual=${count_users} <> expect=7)\n"
    exit 1
fi
printf "...Passed\n"

printf "[test_update_user] "
for uuid in $(call_user_list | jq --raw-output ".users[].uuid" | tail -5); do
    if [ $(call_user_update "${uuid}" '{"name": "fake1"}' 2>/dev/null) != '{"message":"updated"}' ]; then
        printf "...Failed\n"
        exit 1
    fi
done
if [ ${count_users} != 7 ]; then
    printf "...Failed (count_user: actual=${count_users} <> expect=7)\n"
    exit 1
fi
printf "...Passed\n"

printf "[test_delete_user] "
for uuid in $(call_user_list | jq --raw-output ".users[].uuid" | tail -5); do
    if [ $(call_user_delete "${uuid}" 2>/dev/null) != '{"message":"deleted"}' ]; then
        printf "...Failed\n"
        exit 1
    fi
done
count_users_after_delete=$(call_user_list | jq --raw-output ".total")
if [ ${count_users_after_delete} != 2 ]; then
    printf "...Failed (count_user: actual=${count_users_after_delete} <> expect=2)\n"
    exit 1
fi
printf "...Passed\n"

printf "[test_get_user] "
if [ "$(call_user_get $(call_user_list | jq --raw-output ".users[].uuid" | tail -1))" == '{"error":"User not found"}' ]; then
    printf "...Failed\n"
    exit 1
fi
printf "...Passed\n"

printf "[test_get_user_by_wrong_uuid_format] "
if [ "$(call_user_get -1)" != '{"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]}' ]; then
    printf "...Failed\n"
    exit 1
fi
printf "...Passed\n"

printf "[test_get_user_by_user_not_found] "
if [ "$(call_user_get accfd78c-f0dc-4683-90bb-d63de643e852)" != '{"error":"User not found"}' ]; then
    printf "...Failed\n"
    exit 1
fi
printf "...Passed\n"
