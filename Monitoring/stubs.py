import os
import redis
from config import rds, HOST_ID

def get_vm_ids():
    # TODO (ramneek): Get this from redis
    # vm_ids = rds.smembers(f"vms_in_host:{HOST_ID}")
    # return vm_ids
    return ['vm1']


def get_vm_pid(vm_id: str) -> int:
    # TODO (ramneek): Get this from redis
    # return rds.hget(f"vm_configs:{vm_id}", 'pid')
    return 71524
    return os.getpid()

def get_vm_tap_device(vm_id: str) -> str:
    # TODO (ramneek): Get this from redis
    # return rds.hget(f"vm_configs:{vm_id}", 'tap_device')
    return 'eth0'

def get_host_tap_device():
    pass

# Add other things needed, this will be replaced later, possibly with database calls as we get info. from other teams
