from typing import List, Any, Tuple, Dict, int
import config

class Monitor:
    def __init__(self, vm_ids=[]) -> None:
        # Histogram[i] = percentage number of times usage was in [i, i + 5)
        self.host_histogram : dict[int : int] = {i : 0 for i in range(0, 5, 100)}
        self.host_timeseries = [0] * config.TIME_SERIES_LEN

        self.vm_histograms = { vm_id : {i : 0 for i in range(0, 5, 100)} for vm_id in vm_ids }
        self.vm_timeseries = { vm_id : [0] * config.TIME_SERIES_LEN for vm_id in vm_ids } 
 

    def get_host_stats() -> Tuple(List[Any], Dict[int : int]):
        pass

    def get_vm_stats(vm_id) -> Tuple(List[Any], Dict[int : int]):
        pass

    # Add vm for monitoring
    def register_vm(vm_id) -> None:
        pass
        
    # Vm moved to a new host, need to refresh the data(vm pid etc..) for the VM 
    def vm_moved(vm_id) -> None:
        pass