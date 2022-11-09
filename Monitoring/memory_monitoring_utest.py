import unittest
import subprocess
import os
import signal
from config import VMM_REF_DIR
from memory_monitoring import MemoryMonitor
from CustomLogger import setup_custom_logger
logging = setup_custom_logger("logging", os.path.basename(__file__))

class SimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.p = subprocess.Popen(
            ['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100',
             '--memory size_mib=512'], cwd=VMM_REF_DIR)
        # Find this new vm process id

        self.mem_monitor = MemoryMonitor()

    def test_cpu_stats(self):
        # assert vm is created or not.
        self.assertIsNotNone(self.p)

        vm1_id = self.p.pid

        self.mem_monitor.vm_ids.append(f'{vm1_id}')

        # now collect stats
        stat = self.mem_monitor.collect_stats()

        # print stats
        logging.info(f"stats: ({stat[0]} bytes, {stat[1]} )")

        # created vm is not under use.
        self.assertAlmostEqual(0, list(stat[1].values())[0], 1)

        # create vm's
        p2 = subprocess.Popen(
            ['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100',
             '--memory size_mib=512'], cwd=VMM_REF_DIR)

        # assert vm is created or not.
        self.assertIsNotNone(p2)

        # get all vm's ids
        vm2_id = p2.pid

        # allocate the vm-ids
        self.mem_monitor.vm_ids.append(f'{vm1_id}')
        self.mem_monitor.vm_ids.append(f'{vm2_id}')

        # now collect stats
        stat = self.mem_monitor.collect_stats()

        # vm is not under use.
        self.assertAlmostEqual(0, list(stat[1].values())[1], 1)

        # print stats
        logging.info(f"stats: ({stat[0]} bytes, {stat[1]} )")

        # kill all processes
        kill(vm1_id)
        kill(vm2_id)


def kill(proc_pid):
    logging.info(f"killed vm")
    os.kill(proc_pid, signal.SIGTERM)


if __name__ == '__main__':
    unittest.main()

