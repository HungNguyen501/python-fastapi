python-api-template
===

![Github badge](https://badgen.net/badge/icon/github?icon=github&label)
![Python badge](https://badgen.net/pypi/python/black)
![Test badge](https://badgen.net/badge/test%20coverage/100%25/green)

Table of contents:

[1. Introduction](#1-introduction)<br>
[2. Development guide](#2-developement-guide)<br>

# 1. Introduction
The project shows an example for Python-Api-Template that contains 3 components:
- API services
- Postgres database
- Redis

# 2. Developement guide
- Bazel
```bash
$ bazel --version
bazel 7.2.1
```
- Start docker-compose:
```bash
$ make start_docker_compose
Docker compose up...
[+] Running 4/4
 ✔ Network python_api_template        Created                                                                                                    0.1s 
 ✔ Container postgres_for_python_api  Healthy                                                                                                   10.9s 
 ✔ Container redis_for_python_api     Healthy                                                                                                   10.9s 
 ✔ Container python_api               Started                                                                                                   11.0s
# Check active docker containers
$ docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS                      PORTS                      NAMES
32baccce4f23   python_api   "uvicorn src.api.app…"   31 seconds ago   Up 20 seconds (unhealthy)   127.0.0.1:8009->8009/tcp   python_api
6456abb5c3cf   postgres     "docker-entrypoint.s…"   31 seconds ago   Up 30 seconds (healthy)     127.0.0.1:5432->5432/tcp   postgres_for_python_api
bea8c5ec53b9   redis        "docker-entrypoint.s…"   31 seconds ago   Up 30 seconds (healthy)     127.0.0.1:6379->6379/tcp   redis_for_python_api
```

- Host: http://127.0.0.1:8009/api/v1
- Swagger UI: http://127.0.0.1:8009/docs

- Run integration tests
```bash
$ make run_integration_tests
```

<details>
<summary>Click here to see output</summary>

```bash
► Start integration tests...
 connected 
-----------
         1
(1 row)

OK
Redis: count keys=0
⇨ Test api_health_check
__Passed__: actual={"message":"200 OK"} == expected={"message":"200 OK"}
⇨ Test empty user_list
__Passed__: actual={"total":0,"count":0,"users":[]} == expected={"total":0,"count":0,"users":[]}
⇨ Test create_user
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual={"message":"created"} == expected={"message":"created"}
__Passed__: actual=3 == expected=3
⇨ Test user_login
__Passed__: actual=bearer == expected=bearer
__Passed__: actual={"error":"Incorrect username or password"} == expected={"error":"Incorrect username or password"}
⇨ Test update_user
__Passed__: actual={"message":"updated"} == expected={"message":"updated"}
__Passed__: actual=3 == expected=3
⇨ Test update_username
__Passed__: actual={"detail":[{"type":"missing","loc":["body","password"],"msg":"Field required","input":{"username":"f8"}}]} == expected={"detail":[{"type":"missing","loc":["body","password"],"msg":"Field required","input":{"username":"f8"}}]}
⇨ Test update_user failed
__Passed__: actual={"error":"Invalid credentials"} == expected={"error":"Invalid credentials"}
⇨ Test delete_user
__Passed__: actual={"message":"deleted"} == expected={"message":"deleted"}
__Passed__: actual=2 == expected=2
⇨ Test get_user
__Passed__: actual=$2b$12$eeeeeeeeeeeeeeeeeeeeeedJLEz7e/.bs.BVKXsxbOT1ORiO5/EAe == expected=$2b$12$eeeeeeeeeeeeeeeeeeeeeedJLEz7e/.bs.BVKXsxbOT1ORiO5/EAe
⇨ Test get_user by invalid credentials
__Passed__: actual={"error":"Invalid credentials"} == expected={"error":"Invalid credentials"}
► Done integration test!
```
</details>

- Stop docker-compose
```bash
$ make stop_docker_compose
Docker compose down...
[+] Running 4/4
 ✔ Container python_api               Removed                                                                                                    0.6s 
 ✔ Container redis_for_python_api     Removed                                                                                                    0.2s 
 ✔ Container postgres_for_python_api  Removed                                                                                                    0.2s 
 ✔ Network python_api_template        Removed                                                                                                    0.1s 
```
