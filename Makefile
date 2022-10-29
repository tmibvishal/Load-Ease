# Add unit testing here

rpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. mon.proto

vmm:
	# export VMM_REF=$(shell pwd)/vmm-reference
	yes | if [ -d "vmm-reference" ]; then rm -rf vmm-reference; fi
	git clone https://github.com/codenet/vmm-reference.git
	wget https://raw.githubusercontent.com/codenet/understanding-rust-vmm/main/bzimage-hello-busybox -P ./vmm-reference/
	cd vmm-reference && cargo build

clean:
	rm mon_pb2.py
	rm mon_pb2_grpc.py
	yes | if [ -d "vmm-reference" ]; then rm -rf vmm-reference; fi