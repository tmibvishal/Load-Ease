import unittest
import subprocess
import logging
import os
import signal
from config import VMM_REF_DIR
from memory_monitoring import MemoryMonitor
  
class SimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.p = subprocess.Popen(['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100', '--memory size_mib=512'], cwd=VMM_REF_DIR)
        # Find this new vm process id
        
        self.mem_monitor = MemoryMonitor()

    def test_start(self):
        self.assertTrue(True)
        self.p.terminate()

    def test_mem_stats(self):

        # create vm's
        p2 = subprocess.Popen(['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100', '--memory size_mib=512'], cwd=VMM_REF_DIR)

        # assert vm is created or not.
        self.assertIsNotNone(self.p)
        self.assertIsNotNone(p2)

        # get all vm's ids
        vm1_id = self.p.pid
        vm2_id = p2.pid

        print(f"vm1_id: {vm1_id}")
        print(f"vm2_id: {vm2_id}")


        # allocate the vm-ids
        self.mem_monitor.vm_ids.append(vm1_id)
        self.mem_monitor.vm_ids.append(vm2_id)

        # now collect stats
        stat = self.mem_monitor.collect_stats()

        # assert stats

        # self.assertTrue(isinstance(stat, tuple))
        # self.assertTrue(2 == len(stat))
        self.assertIsNotNone(stat[0])
        # self.assertTrue(isinstance(stat[1], dict))
        self.assertIsNotNone(stat[1])

        # print stats
        print(f"stats: {stat}")

        # kill all processes
        kill(vm1_id)
        kill(vm2_id)

def kill(proc_pid):
    logging.getLogger().setLevel(logging.INFO)
    logging.info(f"kill vm-{proc_pid}")
    os.kill(proc_pid, signal.SIGTERM)

if __name__ == '__main__':
    unittest.main()

