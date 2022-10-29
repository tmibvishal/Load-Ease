import os
import uuid
from datetime import datetime
from redis_config import rds
from config import HOST_ID



def get_vm_ids():
    vm_ids = rds.smembers(f"vms_in_host:{HOST_ID}")
    return [vm_id.decode('utf-8') for vm_id in vm_ids]


def get_vm_pid(vm_id: str) -> int:
    return int(rds.hget(f"vm_configs:{vm_id}", 'pid'))

def get_vm_tap_device(vm_id: str) -> str:
    return rds.hget(f"vm_configs:{vm_id}", 'tap_device').decode('utf-8')


def get_host_tap_device():
    return rds.hget(f"host_configs:{HOST_ID}", 'tap_device').decode('utf-8')

# Add other things needed, this will be replaced later, possibly with database calls as we get info. from other teams
