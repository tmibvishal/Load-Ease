import subprocess
from subprocess import PIPE, DEVNULL

def new_vm(vm_config):
    # assert vm_config is None
    cmd = "stress-ng --vm-bytes 3719174k --vm-keep -m 1"
    cmd = cmd.split()

    p = subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL)

    return p.pid





