from monitor import Monitor
from typing import Any, Dict, List, Tuple, Union
import psutil

class MemoryMonitor(Monitor):
    @staticmethod
    def _get_all_vm_stats() -> Dict[str, Union[str, int, float]]:
        # Reference: https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
        # Iterate over all running process
        total = psutil.virtual_memory().total
        vm_infos = []
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                if 'vmm-reference' in proc.name():
                    vm_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                    vm_info['memory_bytes'] = vm_info['memory_percent'] * total / 100
                    # for k in vm_info:
                    #     vm_info[k] = str(vm_info[k])
                    vm_infos.append(vm_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return vm_infos