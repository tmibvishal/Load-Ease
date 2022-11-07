import subprocess
from subprocess import PIPE, DEVNULL

def new_vm(vm_config):
    cmd = "redis-benchmark -p 9999 -l"
    cmd = cmd.split()

    p = subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL)

    return p.pid





