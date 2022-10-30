import config
import speedtest
import multiprocessing
import os
import psutil

from redis_config import rds

vms_db = [
    {
        "vm_id": "vm1",
        "mem": 1024 * 1024 * 256,
        "cpu": 2,
        "net": 1024 * 1024 * 1,
        "pid": os.getpid(),
        "tap_device": "vmtap1",
        "host_id": config.HOST_ID
    },
    {
        "vm_id": "vm1",
        "mem": 1024 * 1024 * 256,
        "cpu": 2,
        "net": 1024 * 1024 * 1,
        "pid": os.getpid(),
        "tap_device": "vmtap2",
        "host_id": config.HOST_ID
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

    rds.hmset(f"host_configs:{host_id}", host_config)    
    rds.set(f"mon_proxy_addr:{host_id}", f"localhost:{config.MON_PORT}")
    rds.sadd('host_ids', host_id)
    for vm in vms_db:
        rds.sadd(f"vms_in_host:{vm['host_id']}", vm['vm_id'])
        rds.hmset(f"vm_configs:{vm['vm_id']}", vm)