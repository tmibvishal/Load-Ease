import subprocess
from subprocess import PIPE, DEVNULL
import os
from time import sleep

from setup import pgrep

# pp_pp = []



def new_vm(vm_config):
    # assert vm_config is None
    # cmd = "stress-ng --vm-bytes 3719174k --vm-keep -m 1"
    print('new_vm called')
    path = os.path.realpath(__file__)
    dir_path = os.path.dirname(path)
    cmd = f'{dir_path}/memtest'
    cmd = cmd.split()
    pp = subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL)

    # old = set(pgrep('memtest'))
    # os.spawnl(os.P_DETACH, cmd)
    # new = set(pgrep('memtest'))
    #
    # print(f'old: {old}')
    # print(f'new: {new}')
    # created_pid = list(new - old)[0]
    # return int(created_pid)

    return pp.pid





