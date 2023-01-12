python3 -m grpc_tools.protoc -I./protos --python_betterproto_out=./protos_gen  $(find ./protos -name "*.proto")
