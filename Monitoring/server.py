from collections import defaultdict
from typing import Dict, List
import psutil

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
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(available, "available")
    server.serve_forever()
    pass

