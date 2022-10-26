from config import MON_PORT
from setup import setup
from typing import Dict
import psutil
from cpu_monitoring import CpuMonitor
from network_monitoring import NetworkMonitor
from memory_monitoring import MemoryMonitor

from xmlrpc.server import SimpleXMLRPCServer

def available() -> Dict[str, str]:
    mem = psutil.virtual_memory()
    d = {'available' : str(mem.available)}
    return d

def get_vm_infos() -> Dict[str, str]:
    # Reference: https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
    # Iterate over all running process
    total = psutil.virtual_memory().total
    vm_infos = []
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            print(type(proc.pid))
            # print(processName , ' ::: ', processID)
            if 'vmm-reference' in processName:
                vm_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                vm_info['memory_bytes'] = vm_info['memory_percent'] * total / 100
                for k in vm_info:
                    vm_info[k] = str(vm_info[k])
                vm_infos.append(vm_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return vm_infos

# Main function of Monitoring Service
# This script will run in all hosts.
# And will set up RPC Calls / Other API for the Load balancer to use.
if __name__ == '__main__':
    setup()
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


