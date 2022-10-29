import psutil
from stubs import get_vm_pid
from monitor import Monitor
from typing import Tuple, Dict



class CpuMonitor(Monitor):
    def __init__(self, vm_ids=None) -> None:
        super().__init__(vm_ids)
        # psutil cpu_percent gives garbage value on the first run
        # so making an initial call to get rid of it
        if vm_ids is None:
            vm_ids = []
        psutil.cpu_percent(interval=None, percpu=True)
        for vm_id in self.vm_ids:
            vm_pid = get_vm_pid(vm_id)
            psutil.Process(vm_pid).cpu_percent(interval=None)/psutil.cpu_count()
    
    def collect_stats(self) -> Tuple[float, Dict[str, float]]:
        '''
        Returns the average cpu usage of the Host and all the VMs
        '''
        # interval=None means that the cpu usage is calculated
        # since the last call to cpu_percent
        # it is a non-blocking call

        # percpu=True means that the cpu usage is calculated
        # for each core
        host_per_cpu_usage = psutil.cpu_percent(interval=None, percpu=True)
        avg_host_cpu_usage = 0
        for cpu in host_per_cpu_usage:
            avg_host_cpu_usage += cpu
        # cpu_percent returns a list of cpu usage for each core
        # so we need to divide by the number of cores
        # to get the average cpu usage
        avg_host_cpu_usage /= len(host_per_cpu_usage)

        # vm_id to cpu usage
        vm_stats = {}
        for vm_id in self.vm_ids:
            # get the pid of the vm
            vm_pid = get_vm_pid(vm_id)
            # divide by the number of cores to get the average cpu usage
            # because cpu_percent might return a value > 100
            # as it sums up the cpu usage of all the cores
            vm_stats[vm_id] = psutil.Process(vm_pid).cpu_percent(interval=None)/psutil.cpu_count()
        
        return (avg_host_cpu_usage, vm_stats)

    # return the cpu stats, accounting for the effect of network usage
    def collect_stats_network_effect(self, host_stat_net: float,
                vm_stats_net: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        # TODO return the cpu stats, accounting for the effect of network usage
        return self.collect_stats()

