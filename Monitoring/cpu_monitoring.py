from stubs import get_vm_pid
from monitor import Monitor
import psutil
from typing import List, Any, Tuple, Dict, int



class CpuMonitor(Monitor):
    def __init__(self, vm_ids=...) -> None:
        super().__init__(vm_ids)
        psutil.cpu_percent(interval=None, percpu=True)
        for vm_id in self.vm_ids:
            vm_pid = get_vm_pid(vm_id)
            psutil.Process(vm_pid).cpu_percent(interval=None)/psutil.cpu_count()
    
    def collect_stats(self) -> Tuple(float, Dict[str, float]):
        host_per_cpu_usage = psutil.cpu_percent(interval=None, percpu=True)
        avg_host_cpu_usage = 0
        for cpu in host_per_cpu_usage:
            avg_host_cpu_usage += cpu
        avg_host_cpu_usage /= len(host_per_cpu_usage)

        vm_stats = {}
        for vm_id in self.vm_ids:
            vm_pid = get_vm_pid(vm_id)
            vm_stats[vm_id] = psutil.Process(vm_pid).cpu_percent(interval=None)/psutil.cpu_count()
        
        return (avg_host_cpu_usage, vm_stats)

