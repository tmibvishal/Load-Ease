from monitor import Monitor
from stubs import get_vm_tap_device,get_host_tap_device
from typing import List, Any, Tuple, Dict

class NetworkMonitor(Monitor):

    def __init__(self, vm_ids=...) -> None:
        super().__init__(vm_ids)
        # get prev values
        self.prev_host_usage = 0
        self.prev_vm_usage = {vm_id : 0 for vm_id in vm_ids}

    def collect_stats(self) -> Tuple(float, Dict[str:float]):
        # return current used , host, for all vm ids
        # add try catch
        # use stubs for get vm tap device
        try:
            
            hostTap = get_host_tap_device()
            f_rx = open("/sys/class/net/{}/statistics/rx_packets".format(hostTap), "r")
            f_tx = open("/sys/class/net/{}/statistics/tx_packets".format(hostTap), "r")
            host_usage = float(f_rx.read()) + float(f_tx.read()) - prev_host_usage
            prev_host_usage = float(f_rx.read()) + float(f_tx.read())
            vm_usage = {}
            for vm_id in self.vm_ids:
                vmTap = get_vm_tap_device(vm_id)
                f_rx = open("/sys/class/net/{}/statistics/rx_packets".format(vmTap), "r")
                f_tx = open("/sys/class/net/{}/statistics/tx_packets".format(vmTap), "r")
                vm_usage[vm_id] = float(f_rx.read()) + float(f_tx.read()) - self.prev_vm_usage[vm_id] # adding rx and tx
                self.prev_vm_usage[vm_id] = float(f_rx.read()) + float(f_tx.read())

            tot_vm_usage = sum(vm_usage.values())
            vm_usage = {vm_id : 100*(vm_usage[vm_id]/tot_vm_usage) for vm_id in vm_usage}

            return (host_usage, vm_usage)
        
        except:
            print("Error in collecting network stats")
        