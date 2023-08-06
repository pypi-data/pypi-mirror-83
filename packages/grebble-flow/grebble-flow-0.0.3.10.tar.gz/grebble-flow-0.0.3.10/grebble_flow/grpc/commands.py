from pathlib import Path

import pkg_resources


def install_proto():
    import grpc_tools.protoc

    cwd = Path(pkg_resources.resource_filename("grebble_flow", "")).parents[0]
    proto_include = pkg_resources.resource_filename("grebble_flow", "grpc/processor/")
    grpc_tools.protoc.main(
        [
            "grpc_tools.protoc",
            f"--proto_path={cwd}",
            "--python_out=./",
            "--grpc_python_out=./",
            f"{proto_include}processor.proto",
        ]
    )
