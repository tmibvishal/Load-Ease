import os
import pdb
import speedtest
import multiprocessing
import psutil
from Monitoring import config
from LoadBalancing.utils import get_ip
from SnapshotTeam.app import start_vm_listener_flask_server
from SnapshotTeam.main import start_vms
from redis_config import rds
from redis_functions import get_new_host_id, get_current_host_id

vms_db = [
    {
        'mem': 1024 * 1024 * 256,
        'cpu': 2,
        'net': 1024 * 1024 * 1,
        'tap_device': 'vmtap1',
        'vm_id' : 0,
        'pid' : os.getpid(),
    },
    {
        'mem': 1024 * 1024 * 256,
        'cpu': 2,
        'net': 1024 * 1024 * 1,
        'tap_device': 'vmtap2',
        'vm_id' : 1,
        'pid' : os.getpid()
    },
]


def clean(host_id: int) -> None:
    """
    Cleans the entire host_id from Redis
    :param host_id:
    :return:
    """

    # Removing all the VMs associated with this host
    st = rds.smembers(f'vms_in_host:{host_id}')
    for vm_id in st:
        d = rds.hgetall(f'vm_configs:{vm_id}')
        pid = int(d['pid'])
        # proc = psutil.Process(pid)
        # if 'vmm-reference' in proc.name():
        #    proc.terminate()
        rds.delete(f'vm_configs:{vm_id}')
    rds.delete(f'mon_proxy_addr:{host_id}')
    rds.delete(f'host_configs:{host_id}')
    rds.delete(f'vmm_proxy_addr:{host_id}')
    rds.delete(f'vms_in_host:{host_id}')
    rds.hdel(f'host_id_to_ip', host_id)
    rds.srem(f'host_ids', str(host_id))


def test_setup():
    rds.flushall()
    host_id = get_current_host_id(check_existence=False)
    if host_id != -1:
        clean(host_id)

    # speed_test = speedtest.Speedtest()
    # tot_bytes = speed_test.download()
    # config.HOST_PEAK_NET_BIT_RATE = tot_bytes
    config.HOST_PEAK_NET_BIT_RATE = 10000000

    # populate redis with host config
    # pdb.set_trace()
    host_id = get_new_host_id()
    host_config = {
        'cpu': multiprocessing.cpu_count(),
        'mem': psutil.virtual_memory().total,
        'net': config.HOST_PEAK_NET_BIT_RATE
    }

    vm_listener_port = 5015
    host_ip = get_ip()
    rds.set(f'vmm_proxy_addr:{host_id}', f'{host_ip:{vm_listener_port}}')
    rds.hset(f'host_configs:{host_id}', mapping=host_config)
    rds.set(f'mon_proxy_addr:{host_id}', f'{host_ip}:{config.MON_PORT}')
    rds.sadd('host_ids', host_id)
    rds.hset(f'host_id_to_ip', key=host_id, value=host_ip)
    # start_vm_listener_flask_server(vm_listener_port)

    for vm in vms_db:
        rds.sadd(f'vms_in_host:{host_id}', vm['vm_id'])
        rds.hmset(f'vm_configs:{vm["vm_id"]}', vm)



def setup():
    # TODO: Flush everything related to this server

    # TODO: put back speedtest

    host_id = get_current_host_id(check_existence = False)
    if host_id != -1:
        clean(host_id)

    # speed_test = speedtest.Speedtest()
    # tot_bytes = speed_test.download()
    # config.HOST_PEAK_NET_BIT_RATE = tot_bytes
    config.HOST_PEAK_NET_BIT_RATE = 10000000

    # populate redis with host config
    # pdb.set_trace()
    host_id = get_new_host_id()
    host_config = {
        'cpu': multiprocessing.cpu_count(),
        'mem': psutil.virtual_memory().total,
        'net': config.HOST_PEAK_NET_BIT_RATE
    }

    vm_listener_port = 5015
    host_ip = get_ip()
    rds.set(f'vmm_proxy_addr:{host_id}', f'{host_ip:{vm_listener_port}}')
    rds.hset(f'host_configs:{host_id}', mapping=host_config)
    rds.set(f'mon_proxy_addr:{host_id}', f'{host_ip}:{config.MON_PORT}')
    rds.sadd('host_ids', host_id)
    rds.hset(f'host_id_to_ip', key=host_id, value=host_ip)
    # pdb.set_trace()
    start_vms(vms_db)
    # start_vm_listener_flask_server(vm_listener_port)
    # for vm in vms_db:
    #     rds.sadd(f'vms_in_host:{vm['host_id']}', vm['vm_id'])
    #     rds.hmset(f'vm_configs:{vm['vm_id']}', vm)


if __name__ == '__main__':
    setup()
