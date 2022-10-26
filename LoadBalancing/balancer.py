import config
from config import rds, migration_lock
from utils import get_top_perc, deserialize_rds_dict, deserialize_rds_str_list
from typing import Dict, List, str, Any
from xmlrpc.client import ServerProxy
import uuid

class LoadBalancer():
    # Don't initialize like this (moved to redis)
    def __init__(self, host_configs : Dict[str, Dict[str : Any]]) -> None:
        self.host_configs = host_configs
        self.vms_in_host : Dict[str, List[str]] = {host_id : [] for host_id in host_configs.keys()}
        self.vm_configs : Dict[str, Dict] = {}

        self.mons : Dict[str, ServerProxy] = {
                host_id : ServerProxy(f"http://{host_cfg['ip']}:{config.MON_PORT}/)") 
                for (host_id, host_cfg) in host_configs.items()
            }

    def __init__(self) -> None:
        self.host_ids : List[str] = []
        self.host_configs = {}
        self.vms_in_host : Dict[str, List[str]] = {}
        self.vm_configs : Dict[str, Dict] = {}
        self.mons : Dict[str, ServerProxy] = {}


    # Assumes caller has migration lock
    def provision(self, vm_config) -> str:
        # Build latest state from redis
        self.host_ids = deserialize_rds_str_list(rds.smembers("host_ids"))
        self.host_configs = {}
        for host_id in self.host_ids:
            self.host_configs[host_id] = deserialize_rds_dict(rds.hgetall(f"host_configs:{host_id}"))

        self.vms_in_host = {}
        self.vm_configs = {}
        for host_id in self.host_ids:
            self.vms_in_host[host_id] = deserialize_rds_str_list(rds.smembers(f"vms_in_host:{host_id}"))
            for vm_id in self.vms_in_host[host_id]:
                self.vm_configs[vm_id] = deserialize_rds_dict(rds.hgetall(f"vm_configs:{vm_id}"))
                for key, val in self.vm_configs[vm_id].items():
                    self.vm_configs[vm_id][key] = int(val)

        self.mons = {}
        for host_id in self.host_ids:
            proxy_addr = rds.get(f"mon_proxy_addr:{host_id}").decode()
            self.mons[host_id] = ServerProxy(proxy_addr)

        # Get best host
        host_id = self.get_best_host(vm_config)

        return host_id

    
    def get_best_host_cpu_mem(self, vm_config):

        mem_vm_stats = {host_id: host_mon.get_vm_mem_stats() for host_id, host_mon in self.mons}
        mem_host_stats = {host_id: host_mon.get_host_mem_stats() for host_id, host_mon in self.mons}

        cpu_vm_stats = {host_id: host_mon.get_vm_cpu_stats() for host_id, host_mon in self.mons}
        cpu_host_stats = {host_id: host_mon.get_host_cpu_stats() for host_id, host_mon in self.mons}

        # Try to provision based on SLA
        best_host = None
        best_val = -(10 ** 20)
        for host_id, vm_ids in self.vms_in_host:
            # All the SLA memory allocated to the VMs in this host
            total_vm_sla_mem = sum([self.vm_configs[vm_id]['mem'] for vm_id in vm_ids])
            leftover_sla_mem = self.host_configs['mem'] - total_vm_sla_mem

            # All the SLA vCPUs to the VMs in this host
            total_vm_sla_cpu = sum([self.vm_configs[vm_id]['cpu'] for vm_id in vm_ids])
            leftover_sla_cpu = self.host_configs['cpu'] - total_vm_sla_cpu

            if leftover_sla_mem >= vm_config['mem'] and leftover_sla_cpu >= vm_config['cpu']:
                # Prioritize the amount of SLA memory left
                if leftover_sla_mem > best_val:
                    best_host = host_id
                    best_val = leftover_sla_mem


        if best_host is not None:
            return best_host


        # Try to provision based on peak usage
        best_host = None
        best_val = -(10 ** 20)

        for host_id, vm_stats in mem_vm_stats.items():
            total_vm_mem_peak_usage = 0
            for vm_id, (_, vm_hist) in vm_stats.items():
                peak_usage = get_top_perc(vm_hist, 0.95) * self.vm_configs[vm_id]['mem']
                total_vm_mem_peak_usage += peak_usage

            total_mem_leftover = self.host_configs[host_id]['mem'] - total_vm_mem_peak_usage

            total_vm_cpu_peak_usage = 0
            for vm_id, (_, vm_hist) in cpu_vm_stats.items():
                peak_usage = get_top_perc(vm_hist, 0.95) * self.host_configs[host_id]['cpu']
                total_vm_cpu_peak_usage += peak_usage

            total_cpu_leftover = self.host_configs[host_id]['cpu'] - total_vm_cpu_peak_usage


            if total_mem_leftover >= vm_config['mem'] and total_cpu_leftover >= vm_config['cpu']:
                if total_mem_leftover > best_val:
                    best_host = host_id
                    best_val = total_mem_leftover
        
        if best_host is not None:
            return best_host


        # Try to provision based peak host usage
        best_host = None
        best_val = -(10 ** 20)

        for host_id, (_, host_hist) in mem_host_stats.items():
            # mem_hist, swap_hist = get_mem_swap_hist(host_hist)
            # peak_host_mem_usage = get_top_perc(mem_hist, 0.95)
            peak_host_mem_usage = get_top_perc(host_hist, 0.95)
            
            peak_host_cpu_usage = get_top_perc(cpu_host_stats[host_id][1], 0.95)
            leftover_peak_cpu = self.host_configs[host_id]['cpu'] * (1 - peak_host_cpu_usage)

            
            if peak_host_mem_usage >= 0.5:
                # this means swap was used and memory was full 
                continue
            else:
                leftover_peak_mem = (1 - peak_host_mem_usage * 2) * self.host_configs[host_id]['mem']
                if leftover_peak_mem >= vm_config['mem'] and leftover_peak_cpu >= vm_config['cpu']:
                    if leftover_peak_mem > best_val:
                        best_host = host_id
                        best_val = leftover_peak_mem
        
        if best_host is not None:
            return best_host

        # Nothing worked return None, we will try to provision only based no memory now.
        return None



    def get_best_host_mem(self, vm_config):

        mem_vm_stats = {host_id: host_mon.get_vm_mem_stats() for host_id, host_mon in self.mons}
        mem_host_stats = {host_id: host_mon.get_host_mem_stats() for host_id, host_mon in self.mons}

        # Try to provision based on SLA
        best_host = None
        best_val = -(10 ** 20)
        for host_id, vm_ids in self.vms_in_host:
            total_vm_sla_mem = sum([self.vm_configs[vm_id]['mem'] for vm_id in vm_ids])
            leftover_sla_mem = self.host_configs['mem'] - total_vm_sla_mem
            if leftover_sla_mem >= vm_config['mem'] and leftover_sla_mem > best_val:
                best_host = host_id
                best_val = leftover_sla_mem
        

        if best_host is not None:
            return best_host


        # Try to provision based on peak usage
        best_host = None
        best_val = -(10 ** 20)

        for host_id, vm_stats in mem_vm_stats.items():
            total_vm_peak_usage = 0
            for vm_id, (_, vm_hist) in vm_stats.items():
                peak_usage = get_top_perc(vm_hist, 0.95) * self.vm_configs[vm_id]['mem']
                total_vm_peak_usage += peak_usage

            total_mem_leftover = self.host_configs[host_id]['mem'] - total_vm_peak_usage
            if total_mem_leftover >= vm_config['mem'] and total_mem_leftover > best_val:
                best_host = host_id
                best_val = total_mem_leftover
        
        if best_host is not None:
            return best_host


        # Try to provision based peak host usage
        best_host = None
        best_val = -(10 ** 20)

        for host_id, (_, host_hist) in mem_host_stats.items():
            # mem_hist, swap_hist = get_mem_swap_hist(host_hist)
            # peak_host_usage = get_top_perc(mem_hist, 0.95)
            peak_host_usage = get_top_perc(host_hist, 0.95)
            
            if peak_host_usage >= 0.5:
                # this means swap was used and memory was full 
                continue
            else:
                leftover_peak_mem = (1 - peak_host_usage * 2) * self.host_configs[host_id]['mem']
                if leftover_peak_mem >= vm_config['mem'] and leftover_peak_mem > best_val:
                    best_host = host_id
                    best_val = leftover_peak_mem
        
        if best_host is not None:
            return best_host

        # Nothing worked, provision based on min. current usage

        # Can be improved to take into account total mem and swap space at each host,
        # but for now this works

        best_host = None
        best_val = 10 ** 20

        for host_id, (host_timeseries, _) in mem_host_stats.items():
            curr_usage = host_timeseries[-1]
            if curr_usage < best_val:
                best_host = host_id
                best_val = curr_usage            

        return best_host



    def get_best_host(self, vm_config) -> str:
        best_host = self.get_best_host_cpu_mem(vm_config)

        if best_host != None:
            return best_host

        best_host = self.get_best_host_mem(vm_config)

        assert(best_host != None)

        return best_host

    
vm_provioner = LoadBalancer()

import vmm_backend

def create_vm(vm_config):
    with migration_lock:
        host_id = vm_provioner.get_best_host(vm_config)
        vm_id = str(uuid.uuid4())

        vm_config['vm_id'] = vm_id
        vm_config['host_id'] = host_id

        resp = vmm_backend.create_vm_request(vm_config)

        for k,v in resp.items():
            vm_config[k] = v

        pid = resp['pid']
        tap_device = resp['tap_device']
        rpc_port = resp['rpc_port']
        # TODO create call in monitoring services to add new vm

        # Add vm info. in redis
        rds.hset(f'vm_config:{vm_id}', mapping=vm_config)

    return vm_config


