rpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. mon.proto
clean:
	rm mon_pb2.py
	rm mon_pb2_grpc.py