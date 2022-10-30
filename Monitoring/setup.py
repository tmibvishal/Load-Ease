import config
import speedtest
import multiprocessing
import os
import psutil

from LoadBalancing.utils import get_ip
from SnapshotTeam.app import start_vm_listener_flask_server
from SnapshotTeam.main import start_vms
from redis_config import rds

vms_db = [
    {
        "mem": 1024 * 1024 * 256,
        "cpu": 2,
        "net": 1024 * 1024 * 1,
        "tap_device": "vmtap1"
    },
    {
        "mem": 1024 * 1024 * 256,
        "cpu": 2,
        "net": 1024 * 1024 * 1,
        "tap_device": "vmtap2"
    },
]


def setup():
    speed_test = speedtest.Speedtest()
    tot_bytes = speed_test.download()
    config.HOST_PEAK_NET_BIT_RATE = tot_bytes

    # populate redis with host config
    host_id = config.HOST_ID
    host_config = {
        'cpu': multiprocessing.cpu_count(),
        'mem': psutil.virtual_memory().total,
        'net': config.HOST_PEAK_NET_BIT_RATE
    }

    vm_listener_port = 8010
    rds.set(f'vmm_proxy_addr:{host_id}', f'{get_ip():{vm_listener_port}}')
    rds.hmset(f"host_configs:{host_id}", host_config)    
    rds.set(f"mon_proxy_addr:{host_id}", f"{get_ip()}:{config.MON_PORT}")
    rds.sadd('host_ids', host_id)
    start_vms(vms_db)
    start_vm_listener_flask_server(vm_listener_port)
    # for vm in vms_db:
    #     rds.sadd(f"vms_in_host:{vm['host_id']}", vm['vm_id'])
    #     rds.hmset(f"vm_configs:{vm['vm_id']}", vm)