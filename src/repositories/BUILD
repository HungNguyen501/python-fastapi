py_library(
    name = "base_repository",
    srcs = ["base_repository.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "user_repository",
    srcs = ["user_repository.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_base_repository",
    srcs = ["tests/test_base_repository.py"],
    main = "tests/test_base_repository.py",
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
        "//src/repositories:base_repository",
    ],
)

py_test(
    name = "test_user_repository",
    srcs = ["tests/test_user_repository.py"],
    main = "tests/test_user_repository.py",
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
        "//src/repositories:user_repository",
        "//src/repositories:base_repository",
        "//src/db:database",
    ],
)
