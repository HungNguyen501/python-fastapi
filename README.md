python-api-template
===

![Github badge](https://badgen.net/badge/icon/github?icon=github&label)
![Python badge](https://badgen.net/pypi/python/black)
![Test badge](https://badgen.net/badge/test%20coverage/100%25/green)

Table of contents:

[1. Introduction](#1-introduction)<br>
[2. Development guide](#2-developement-guide)<br>
[3. Three Layer Architecture](#3-three-layer-architecture)<br>
[4. CI flow](#4-ci-flow)<br>
[5. API docs](#5-api-docs)<br>


# 1. Introduction
The source code shows an example for Python-Api-Template that contains 2 components:
- API services
- Postgres database

Otherwise, it strictly enforces following conventions:
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- PEP8 standards
- Unit tests - Code coverage reaches `100%`
- Capturing incremental changes for CI-flow

# 2. Developement guide
- Start docker-compose:
```bash
$ make start_docker_compose
Docker compose up...
[+] Running 2/2
 ✔ Container postgres_for_python_api  Healthy                                                                                                     0.5s 
 ✔ Container python_api               Running
# Check active docker containers
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED         STATUS                            PORTS                      NAMES
1ce6d34f6a9d   python_api   "uvicorn src.api.app…"   4 seconds ago   Up 2 seconds (health: starting)   127.0.0.1:8009->8009/tcp   python_api
608899aa0824   postgres     "docker-entrypoint.s…"   30 hours ago    Up 30 hours (healthy)             127.0.0.1:5432->5432/tcp   postgres_for_python_api
```

- Run integration tests
```bash
$ make run_integration_tests
```

<details>
<summary>Click here to see output</summary>

```bash
connected 
-----------
         1
(1 row)

⇨ Test api_health_check
__Passed__: actual={"message":"200 OK"} == expected={"message":"200 OK"}
⇨ Test empty user_list
__Passed__: actual={"total":0,"count":0,"users":[]} == expected={"total":0,"count":0,"users":[]}
⇨ Test create_user
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual=7 == expected=7
⇨ Test update_user
__Passed__: actual={"message":"updated"} == expected={"message":"updated"}
__Passed__: actual={"message":"updated"} == expected={"message":"updated"}
__Passed__: actual={"message":"updated"} == expected={"message":"updated"}
__Passed__: actual={"message":"updated"} == expected={"message":"updated"}
__Passed__: actual={"message":"updated"} == expected={"message":"updated"}
__Passed__: actual=7 == expected=7
⇨ Test update_user by wrong uuid format
__Passed__: actual={"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]} == expected={"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]}
⇨ Test update_user by not found uuid
__Passed__: actual={"error":"User not found"} == expected={"error":"User not found"}
⇨ Test update_user by wrong schema
__Passed__: actual={"error":"null value in column "name" of relation "users" violates not-null constraint"} == expected={"error":"null value in column "name" of relation "users" violates not-null constraint"}
⇨ Test delete_user
__Passed__: actual={"message":"deleted"} == expected={"message":"deleted"}
__Passed__: actual={"message":"deleted"} == expected={"message":"deleted"}
__Passed__: actual={"message":"deleted"} == expected={"message":"deleted"}
__Passed__: actual={"message":"deleted"} == expected={"message":"deleted"}
__Passed__: actual={"message":"deleted"} == expected={"message":"deleted"}
__Passed__: actual=2 == expected=2
⇨ Test get_user
__Passed__: actual=user2 == expected=user2
⇨ Test get_user by wrong uuid format
__Passed__: actual={"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]} == expected={"detail":[{"type":"uuid_parsing","loc":["query","uuid"],"msg":"Input should be a valid UUID, invalid group count: expected 5, found 2","input":"-1","ctx":{"error":"invalid group count: expected 5, found 2"}}]}
⇨ Test get_user by not found user
__Passed__: actual={"error":"User not found"} == expected={"error":"User not found"}
► Done integration test!
```
</details>

- Stop docker-compose
```bash
$ make stop_docker_compose
Docker compose down...
[+] Running 3/3
 ✔ Container python_api               Removed                                                                                                     0.5s 
 ✔ Container postgres_for_python_api  Removed                                                                                                     0.2s 
 ✔ Network python_api_template        Removed                                                                                                     0.2s
```

# 3. Three Layer Architecture
```bash
$ tree -L 1 src/
src/
├── api
├── common
├── db
├── repositories
├── schemas
└── services
```
## Interface layer
The interface layer includes `api` module and `schemas` module. That should define API endpoints and interact with service layer.

## Service layer
The service layer includes `services` module. That should store business logic. Service layer acts as an intermediate layer between the Interface layer and Database layer.

## Database layer
The database layer includes `repositories` module and `db` module. That should contain database connectors, data models. This layer accepts the processed data from the service layer and perform queries and operations to interact with the database.

# 4. CI flow
<p style="text-align:center;"><img src="./ci/images/github-ci.png" width="80%" /></p>

The image above illustrates CI-flow. In particular,
- `Install environments`: set up OS, Git env, also, install Bazel.
- `Check incremental changes`: get changed files from Git and detect dependencies by Bazel. After that, it verifies Pep8 convention and runs unit tests that qualifies 100% code coverage as criteria.
- `Build docker compose`: build FastAPI service and Postgres DB
- `Run integration tests`: execute bash script to run test cases.
- `Complete job`: clean up orphan processes.

# 5. API docs
- Host: http://127.0.0.1:8009/api/v1

## Health check
Get API health check

- **URL:** `/health`
- **Method:** `GET`
- **Success Response:**
    - Code: `200`
    - Content:
    ```python
    {
        "message": "200 OK"
    }
    ```

## Create User
Insert user record

- **URL:** `/user`
- **Method:** `POST`
- **Payload**
  ```python
  {
    "name": string
  }
  ```
- **Success Response:**
    - Code: `200`
    - Content:
    ```python
    {
        "message": "created"
    }
    ```
## Update User
Update user information

- **URL:** `/user?uuid={1}`
- **Method:** `PUT`
- **Params**
    - `uuid`(string): uuid of user
- **Payload**
  ```python
  {
    "name": string
  }
  ```
- **Success Response:**
    - Code: `200`
    - Content:
    ```python
    {
        "message": "updated"
    }
    ```
## Delete User
Delete user record

- **URL:** `/user?uuid={1}`
- **Method:** `DELETE`
- **Params**
    - `uuid`(string): uuid of user
- **Success Response:**
    - Code: `200`
    - Content:
    ```python
    {
        "message": "deleted"
    }
    ```

## Get User
Get user information

- **URL:** `/user?uuid={1}`
- **Method:** `GET`
- **Params**:
    - `uuid`(string): uuid of user
- **Success Response:**
    - Code: `200`
    - Content:
    ```python
    {
        "uuid": "a00a0aaa-0aa0-00a0-00aa-0a0aa0aa00a0",
        "name": "alice"
    }
    ```

## List User
Get list of user information

- **URL:** `/user/list?start={1}&page_size={2}`
- **Method:** `GET`
- **Params**:
    - `start`(integer): start index of user list
    - `page_size`(integer): number of records per request
- **Success Response:**
    - Code: `200`
    - Content:
    ```python
    {
        "total": 2,
        "count": 2,
        "users": [
            {
                "name": "user1",
                "uuid": "d785d88d-a8c0-4e3a-8500-9ab68239ecc1"
            },
            {
                "name": "user2",
                "uuid": "16d68d9a-f95d-42b1-9ce6-ddcac019cc57"
            }
        ]
    }
    ```

