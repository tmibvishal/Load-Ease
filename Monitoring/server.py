from config import MON_PORT
from typing import Dict
import psutil
from cpu_monitoring import CpuMonitor
from network_monitoring import NetworkMonitor
from memory_monitoring import MemoryMonitor

from xmlrpc.server import SimpleXMLRPCServer


# Main function of Monitoring Service
# This script will run in all hosts.
# And will set up RPC Calls / Other API for the Load balancer to use.
if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", MON_PORT))
    print("Listening on port 8000...")
    cpumon = CpuMonitor()
    netmon = NetworkMonitor()
    memmon = MemoryMonitor()

    cpumon.start()
    netmon.start()
    memmon.start()

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
    while True:
        print('yo')


