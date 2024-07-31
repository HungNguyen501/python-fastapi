py_library(
    name = "database",
    srcs = ["database.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "models",
    srcs = ["models/base_model.py", "models/user_model.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_database",
    srcs = ["tests/test_database.py"],
    main = "tests/test_database.py",
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
        "//src/db:database",
        "//src/common:configs",
    ],
)
