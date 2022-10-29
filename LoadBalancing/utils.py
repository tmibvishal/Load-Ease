import subprocess
import uuid
import socket
import grpc
import mon_pb2
import mon_pb2_grpc
from rpc_utils import grpcStat2py
from datetime import datetime
from redis_config import rds
from config import VMM_REF_DIR

import sys

from utils import eprint


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

def create_virtual_machine(mem_mb: int, tap_device: str, cpu_cores: int = 1,
                           image_path: str = './bzimage-hello-busybox') -> str:
    """
    :param mem_mb:
    :param tap_device:
    :param cpu_cores:
    :param image_path:
    :return: Returns the VM ID
    """
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
        return ''

    vm_id = uuid.uuid4().hex + datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    # proc = subprocess.Popen(
    #     ['./target/debug/vmm-reference', '--kernel',
    #      'path=./bzimage-hello-busybox', '--net', 'tap=vmtap100',
    #      '--memory', 'size_mib=512'], cwd=VMM_REF_DIR, stdout=subprocess.DEVNULL,
    #     stderr=subprocess.STDOUT)
    proc = subprocess.Popen(
        ['./target/debug/vmm-reference',
         '--kernel', f'path={image_path}',
         '--net', f'tap={tap_device}',
         '--memory', f'size_mib={mem_mb}',
         '--vcpus', f'num={cpu_cores}'],
        cwd=VMM_REF_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    proc.terminate()
    pid = proc.pid

    # Insert all config in Redis
    rds.sadd(f'vms_in_host:{host_id}', vm_id)
    vm_configs = {'mem': mem_mb,
                  'cpu': cpu_cores,
                  'disk': '',
                  'image_path': image_path,
                  'host_id': host_id,
                  'pid': pid,
                  'tap_device': tap_device}
    hkey = f'vm_configs:{vm_id}'
    rds.hset(hkey, mapping=vm_configs)
    return vm_id


def get_top_perc(hist, perc=0.90):
    covered = 0
    for i in range(0, 100, 5):
        covered += hist[i]
        if covered >= perc:
            return (i + 2.5) / 100.0

    if covered == 0.0:
        # hist not filled ?
        return 0.0
    else:
        # 100% usage
        return 1.0


def get_mem_swap_hist(hist):
    mem_hist = {i: 0 for i in range(0, 100, 5)}
    swap_hist = {i: 0 for i in range(0, 100, 5)}

    total_mem_p = 0.0
    total_swap_p = 0.0

    for i in range(0, 5, 50):
        total_mem_p += hist[i]
        total_swap_p += hist[i + 50]

    for i in range(0, 5, 50):
        mem_hist[i * 2] = hist[i] / total_mem_p
        swap_hist[i * 2] = hist[i + 50] / total_swap_p

    return mem_hist, swap_hist


def deserialize_rds_dict(hset):
    ret = {}
    for k, v in hset.items():
        k = k.decode()
        v = v.decode()
        ret[k] = v
        if v.isnumeric():
            ret[k] = int(v)
    return ret


def deserialize_rds_str_list(lst):
    ret = []
    for i in lst:
        i = i.decode()
        ret.append(i)
    return ret


def get_stats(proxy):
    with grpc.insecure_channel(proxy) as channel:
        stub = mon_pb2_grpc.MonitorStub(channel)
        response = stub.GetStats(mon_pb2.Empty())
        return {
            'cpu': grpcStat2py(response.cpu),
            'mem': grpcStat2py(response.mem),
            'net': grpcStat2py(response.swap),
        }
