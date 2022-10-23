from typing import List, Tuple, Dict, Any
import config
from threading import Thread
import time

class Monitor:
    def __init__(self, vm_ids : List[Any]=[]) -> None:
        # Histogram[i] = percentage number of times usage was in [i, i + 5)
        self.vm_ids = vm_ids
        self.host_histogram : dict[int : float] = {i : 0 for i in range(0, 100, 5)}
        self.host_timeseries = []

        self.vm_histograms = { vm_id : {i : 0 for i in range(0, 100, 5)} for vm_id in vm_ids }
        self.vm_timeseries = { vm_id : [] for vm_id in vm_ids }

        self.total_intervals = 0


    def start(self) -> None:
        th = Thread(target=self.update, args=(), daemon=True)
        th.start()

    
    # Inheriting classes implement
    # return (host_usage %, and Dict[vmid : vm usage %])
    # Flaot = Percentage, Ex: 95.2 % -> 95.2 (not 0.952)
    def collect_stats(self) -> Tuple[float, Dict[str, float]]:
        pass


    # Inheriting classes implement
    # Implement in base class, add a new vm for monitoring
    def register_vm(self, vm_id) -> None:
        pass

    # Inheriting classes implement
    # Vm moved to a new host, can remove this vm from monitoring
    # Clean up the datastructures for this vm
    def vm_moved(self, vm_id) -> None:
        pass
        

    def update(self) -> None:
        while True:
            self.total_intervals += 1

            (host_stat, vm_stats) = self.collect_stats()

            for vm_id, usage in vm_stats.items():
                self.update_histogram(vm_id, usage)
                self.update_timeseries(vm_id, usage)

            self.update_histogram(None, host_stat, host=True)
            self.update_timeseries(None, host_stat, host=True)

            time.sleep(config.MONITOR_INTERVAL)


    def update_histogram(self, vm_id, resource_usage, host: bool = False) -> None:
        hist = self.host_histogram
        if not host:
            hist = self.vm_histograms[vm_id]

        for interval in range(0,100,5):
            if resource_usage >= interval and resource_usage < interval + 5:
                hist[interval] = (hist[interval] * (self.total_intervals -1) + 1) / self.total_intervals
            else:
                hist[interval] = (hist[interval] * (self.total_intervals - 1)) / self.total_intervals
      

    def update_timeseries(self, vm_id, resource_usage, host: bool = False) -> None:
        timeseries : List = self.host_timeseries
        if not host:
            timeseries = self.vm_timeseries[vm_id]
        timeseries.append(resource_usage)
        if len(timeseries) > config.TIME_SERIES_LEN:
            timeseries.pop(0)

            
    def get_host_stats(self) -> Tuple[List[float], Dict[int, float]]:
        return self.host_timeseries, self.host_histogram

    def get_vm_stats(self, vm_id: str) -> Tuple[List[float], Dict[int, float]]:
        return self.vm_timeseries[vm_id], self.vm_histograms[vm_id]

