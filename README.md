Python FastAPI Example
===

![Github badge](https://badgen.net/badge/icon/github?icon=github&label)
![Python badge](https://badgen.net/pypi/python/black)
![Test badge](https://badgen.net/badge/test%20coverage/100%25/green)

## 1. Layered architecture
This layered architecture can be seen translated to an application in the following diagram:
```bash
.
├── scripts
│   ├── build
│   └── ci
└── src
    ├── api
    │   └── v1  # Controllers for the api
    ├── common  # Ultility functions
    ├── exceptions  # Exception handler
    ├── infrastructures
    │   ├── databases  # Database initlizations
    │   │   ├── models  # Database models
    │   │   └── sql  # Database migration scripts
    │   └── repositories  # Repositories for interacting with the databases
    ├── schemas  # Marshmallow for schemas
    └── services  # Services for interacting with the domains
        ├── auth
        └── business
```

## 2. Prerequisites
- Bazel
```bash
$ bazel --version
bazel 7.2.1
```
- Flyway
```bash
$ flyway --version
Flyway OSS Edition 11.3.3 by Redgate
```
- Python
```bash
$ python3.12 --version
Python 3.12.9
```

## 3. Developement guide
- Install requirements:
```bash
$ make install
```

- Githook:
```bash
$ make githook  # Add a script to pre-commit in githooks
```

- Docker compose: 
```bash
$ make docker_compose_up
$ make docker_compose_down
```

- Run database migration:
```bash
$ make migrate
```

- Run integration tests:
```bash
$ make run_integration_tests
```

- Host: http://127.0.0.1:8009/api/v1
- Swagger UI: http://127.0.0.1:8009/docs
