def get_vm_pid(vm_id: str) -> int:
import os
def get_vm_pid(vm_id: str) -> int:
    return os.getpid()
    pass

def get_vm_tap_device(vm_id: str) -> str:
def get_vm_tap_device(vm_id: str) -> str:
    return 'eth0'
    pass

def get_host_tap_device():
    pass

# Add other things needed, this will be replaced later, possibly with database calls as we get info. from other teams

