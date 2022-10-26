from typing import Dict
import time
from threading import Thread
from config import MON_PORT, MONITOR_INTERVAL
from cpu_monitoring import CpuMonitor
from network_monitoring import NetworkMonitor
from memory_monitoring import MemoryMonitor

from xmlrpc.server import SimpleXMLRPCServer


def monitoring_thread(cpu_mon: CpuMonitor, mem_mom: MemoryMonitor, net_mon: NetworkMonitor) -> None:
    while True:
        host_stat, vm_stats = mem_mom.collect_stats()
        mem_mom.update(host_stat, vm_stats)

        host_stat, vm_stats = net_mon.collect_stats()
        net_mon.update(host_stat, vm_stats)

        host_stat, vm_stats = cpu_mon.collect_stats_network_effect(host_stat, vm_stats)
        cpu_mon.update(host_stat, vm_stats)
        
        time.sleep(MONITOR_INTERVAL)




# Main function of Monitoring Service
# This script will run in all hosts.
# And will set up RPC Calls / Other API for the Load balancer to use.
if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", MON_PORT))
    print("Listening on port 8000...")
    cpumon = CpuMonitor()
    netmon = NetworkMonitor()
    memmon = MemoryMonitor()

    th = Thread(target=monitoring_thread, args=(cpumon, memmon, netmon), daemon=True)
    th.start()

    server.register_function(cpumon.get_host_stats, 'get_host_cpu_stats')
    server.register_function(cpumon.get_vm_stats, 'get_vm_cpu_stats')

    server.register_function(memmon.get_host_stats, 'get_host_mem_stats')
    server.register_function(memmon.get_vm_stats, 'get_vm_mem_stats')


    server.register_function(netmon.get_host_stats, 'get_host_net_stats')
    server.register_function(netmon.get_vm_stats, 'get_vm_net_stats')

    def register_vm(vm_id : str) -> None:
        cpumon.register_vm(vm_id)
        netmon.register_vm(vm_id)
        memmon.register_vm(vm_id)
    
    server.register_function(register_vm, 'register_vm')
    server.serve_forever()

