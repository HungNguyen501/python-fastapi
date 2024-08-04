python-api-template
===

![Github badge](https://badgen.net/badge/icon/github?icon=github&label)
![Python badge](https://badgen.net/pypi/python/black)
![Test badge](https://badgen.net/badge/test%20coverage/100%25/green)

# 1. Introduction
The source code shows an example for Python-Api-Template that contains 2 components:
- API services
- Postgres database

Otherwise, it strictly enforces following conventions:
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- Qualify PEP8 convention
- Unit tests - Code coverage reaches `100%`
- Capture incremental changes for CI-flow

# 2. Three Layer Architecture
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
The service layer includes `services` module. That should store business logic. Service layer acts as an intermediate layer between the API layer and database layer.

## Database layer
The database layer includes `repositories` module and `db` module. That should contains database connectors, data models. This layer accepts the processed data from the service layer and perform queries and operations to interact with the database.

# 3. CI flow
<p style="text-align:center;"><img src="./ci/images/github-ci.png" width="80%" /></p>

The image above illustrates CI-flow. In particular,
- `Install environments`: set up OS, Git env, also, install Bazel.
- `Check incremental changes`: get changed files from Git and detect dependencies by Bazel. After that, it verifies Pep8 convention and unit tests that qualifies 100% code coverage.
- `Build docker compose`: build FastAPI service and Postgres DB
- `Run integration tests`: execute bash script to run test cases.
- `Complete job`: clean up orphan processes.

# 4. API docs
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

