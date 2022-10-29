# Add unit testing here
default:
	export VMM_REF=$(shell pwd)/vmm-reference
	yes | rm -r vmm-reference
	git clone https://github.com/codenet/vmm-reference.git
	wget https://raw.githubusercontent.com/codenet/understanding-rust-vmm/main/bzimage-hello-busybox -P ./vmm-reference/
	cd vmm-reference && cargo build

