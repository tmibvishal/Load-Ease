import socket
import sys
from typing import List

from LoadBalancing.redis_config import rds


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_ip():
    """
    :return: Returns the IP Address of current system
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_vm_id_with_rpc_port(rpc_port: int) -> str:
    d = rds.hgetall('rpc_ports')
    vm_id = ''
    for k, v in d.items():
        if v == rpc_port:
            vm_id = k
    return vm_id

def get_vm_host_id(vm_id: str) -> int:
    d = rds.hgetall(name=f'vm_configs:{vm_id}')
    host_id = d['host_id']
    assert isinstance(host_id, int)
    return host_id


def get_current_host_id():
    host_ip = get_ip()
    host_id = -1
    d = rds.hgetall(f'mon_proxy_addr')
    for k, v in d.items():
        if v == host_ip:
            host_id = k
            break
    if host_id == -1:
        eprint(f'This host with {host_ip} is not stored in database. '
               f'So, can\'t create a VM')
    return host_id


def get_vm_ids() -> List[str]:
    host_id = get_current_host_id()
    vm_ids = rds.smembers(f"vms_in_host:{host_id}")
    return [vm_id.decode('utf-8') for vm_id in vm_ids]


def get_vm_pid(vm_id: str) -> int:
    # a = int(rds.hget(f"vm_configs:{vm_id}", 'pid'))
    # return a
    return int(vm_id)


def get_vm_tap_device(vm_id: str) -> str:
    a = rds.hget(f"vm_configs:{vm_id}", 'tap_device').decode('utf-8')
    return a


def get_host_tap_device() -> str:
    host_id = get_current_host_id()
    tap_device = rds.hget(f"host_configs:{host_id}", 'tap_device').decode('utf-8')
    return tap_device

# Add other things needed, this will be replaced later,
# possibly with database calls as we get info. from other teams
