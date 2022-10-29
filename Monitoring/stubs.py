import os
import uuid
from datetime import datetime
from config import rds

def create_vm() -> int:
    s = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    s2 = uuid.uuid4().hex

def get_vm_pid(vm_id: str) -> int:
    configs = rds.hgetall(f'vm_configs:{vm_id}')
    return configs['pid']


def get_vm_tap_device(vm_isd: str) -> str:
    return 'eth0'


def get_host_tap_device():
    pass

# Add other things needed, this will be replaced later, possibly with database calls as we get info. from other teams
