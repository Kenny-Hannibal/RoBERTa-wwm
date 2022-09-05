cd ..
python -m grpc_tools.protoc -Ionline/rpc/ --python_out=online/rpc/ --grpc_python_out=online/rpc/ segment.proto