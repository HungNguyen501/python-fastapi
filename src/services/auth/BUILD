py_library(
    name = "auth_service",
    srcs = ["auth_service.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//src/db:database",
        "//src/db:redis_db",
        "//src/common:settings",
    ]
)

py_test(
    name = "test_auth_service",
    srcs = ["tests/test_auth_service.py"],
    main = "tests/test_auth_service.py",
    timeout = "short",
    args = [
        "-vv",
    ],
    tags = [
        "local",
        "requires-network",
        "yourit",
    ],
    deps = [
        "//src/services:auth_service",
        "//src/services:user_service",
        "//src/common:exceptions",
        "//src/common:crypto",
        "//src/common:settings",
        "//src/db:redis_db",
    ],
)
