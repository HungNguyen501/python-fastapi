py_library(
    name = "base_service",
    srcs = ["base_service.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "user_service",
    srcs = ["user_service.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//src/db:database",
        "//src/db:models",
        "//src/common:settings",
    ]
)

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
    name = "test_user_service",
    srcs = ["tests/test_user_service.py"],
    main = "tests/test_user_service.py",
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
        "//src/services:user_service",
        "//src/services:base_service",
        "//src/repositories:user_repository",
        "//src/common:exception_handler",
        "//src/common:exceptions",
    ],
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
