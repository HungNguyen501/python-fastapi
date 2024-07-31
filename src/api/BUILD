py_library(
    name = "application",
    srcs = ["application.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "v1_router",
    srcs = ["v1/router.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "v1_user",
    srcs = ["v1/user.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "v1_health_check",
    srcs = ["v1/health_check.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_application",
    srcs = ["tests/test_application.py"],
    main = "tests/test_application.py",
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
        "//src/api:application",
        "//src/api:v1_router",
        "//src/common:exception_handler",
    ],
)

py_test(
    name = "test_v1_router",
    srcs = ["v1/tests/tes_router.py"],
    main = "v1/tests/tes_router.py",
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
        "//src/api:v1_router",
        "//src/api:v1_user",
        "//src/api:v1_health_check",
    ],
)

py_test(
    name = "test_v1_health_check",
    srcs = ["v1/tests/test_health_check.py"],
    main = "v1/tests/test_health_check.py",
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
        "//src/api:v1_health_check",
    ],
)

py_test(
    name = "test_v1_user",
    srcs = ["v1/tests/test_user.py"],
    main = "v1/tests/test_user.py",
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
        "//src/api:v1_user",
        "//src/services:user_service",
    ],
)
