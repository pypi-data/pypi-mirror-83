import pkg_resources


def install_proto():
    import grpc_tools.protoc

    proto_include = pkg_resources.resource_filename(
        "grebble_flow", "grpc/processor/"
    )

    grpc_tools.protoc.main(
        [
            "grpc_tools.protoc",
            "-I{}".format(proto_include),
            "--python_out=" + proto_include,
            "--grpc_python_out=" + proto_include,
            "processor.proto",
        ]
    )
