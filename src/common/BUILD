py_library(
    name = "configs",
    srcs = ["configs.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "exception_handler",
    srcs = ["exception_handler.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "exceptions",
    srcs = ["exceptions.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_configs",
    srcs = ["tests/test_configs.py"],
    main = "tests/test_configs.py",
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
        "//src/common:configs",
    ],
)

py_test(
    name = "test_exception_handler",
    srcs = ["tests/test_exception_handler.py"],
    main = "tests/test_exception_handler.py",
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
        "//src/common:exception_handler",
        "//src/common:exceptions",
    ],
)

py_test(
    name = "test_exceptions",
    srcs = ["tests/test_exceptions.py"],
    main = "tests/test_exceptions.py",
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
        "//src/common:exceptions",
    ],
)
