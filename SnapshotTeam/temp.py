import subprocess
from subprocess import PIPE, DEVNULL
import os
from time import sleep

pp_pp = []

def new_vm():
    # assert vm_config is None
    # cmd = "stress-ng --vm-bytes 3719174k --vm-keep -m 1"

    path = os.path.realpath(__file__)
    dir_path = os.path.dirname(path)
    cmd = '/Users/vishal/Downloads/iitd_things/9th_Sem/col732_virtualization/project/LoadEase/SnapshotTeam/memtest'
    cmd = cmd.split()
    pp_pp.append(subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL))
    sleep(5)
    return pp_pp[-1].pid

new_vm()
sleep(2)
new_vm()
