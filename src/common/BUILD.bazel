py_library(
    name = "crypto",
    srcs = ["crypto.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "settings",
    srcs = ["settings.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_settings",
    srcs = ["tests/test_settings.py"],
    main = "tests/test_settings.py",
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
        "//src/common:settings",
    ],
)
