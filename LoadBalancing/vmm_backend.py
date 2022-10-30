import requests
from redis_config import rds
import json
from LoadBalancing.utils import deserialize_rds_dict, deserialize_rds_str_list
import uuid

CREATE_END_POINT = 'create'
SNAPSHOT_END_POINT = 'snapshot'


def create_vm_request(host_id, vm_config):
    # request_format = {
    #     'mem': 100,
    #     'cpu': 1,
    #     'disk': 100,
    #     'image_path': 'path',
    #     'create': True
    # }
    request = vm_config.copy()
    request['image_path'] = 'path'
    request['create'] = True

    vmm_proxy_addr = rds.get(f"vmm_proxy_addr:{host_id}").decode()

    resp = requests.post(f'{vmm_proxy_addr}/{CREATE_END_POINT}', json=request).json()
    resp = json.loads(resp)
    print(resp)
    return resp


def migrate_vm(vm_id, new_host_id):

    vm_config = deserialize_rds_dict(rds.hgetall(f'vm_config:{vm_id}'))
    old_host = vm_config['host_id']
    rpc_port = vm_config['rpc_port']

    migratiion_uuid = str(uuid.uuid4())

    # pause vm in old host
    vmm_proxy_addr = rds.get(f"vmm_proxy_addr:{old_host}").decode()

    request = {
        'cpu_snapshot_path': f'/snapshots/{migratiion_uuid}.cpu',
        'memory_snapshot_path': f'/snapshots/{migratiion_uuid}.mem',
        'rpc_port': rpc_port,
        'resume' : False
    }

    resp = requests.post(f'{vmm_proxy_addr}/{SNAPSHOT_END_POINT}', json=request).json()
    resp = json.loads(resp)
    print(resp)


    # start vm in new host
    vmm_proxy_addr = rds.get(f"vmm_proxy_addr:{new_host_id}").decode()

    request = {
        'cpu_snapshot_path': f'/snapshots/{migratiion_uuid}.cpu',
        'memory_snapshot_path': f'/snapshots/{migratiion_uuid}.mem',
        'resume' : True
    }

    resp = requests.post(f'{vmm_proxy_addr}/{CREATE_END_POINT}', json=request).json()
    resp = json.loads(resp)

    print(resp)

    # new_rpc_port = resp['rpc_port']

    # TODO Do all this and update redis in caller
    # vm_config['host_id'] = new_host_id
    # vm_config['rpc_port'] = new_rpc_port 

    return resp