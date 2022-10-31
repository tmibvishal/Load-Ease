import unittest
import subprocess
import logging
import os
import signal
from LoadBalancing.Monitoring.config import VMM_REF_DIR
from LoadBalancing.CustomLogger import setup_custom_logger
from LoadBalancing.Monitoring.network_monitoring import NetworkMonitor

class SimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.p = subprocess.Popen(
            ['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100',
             '--memory size_mib=512'], cwd=VMM_REF_DIR)
        # Find this new vm process id

        self.net_monitor = NetworkMonitor()

    def test_network_stats(self):
        logger = setup_custom_logger("logging", os.path.basename(__file__))
        # assert vm is created or not.
        self.assertIsNotNone(self.p)

        vm1_id = self.p.pid

        self.net_monitor.vm_ids.append(f"{vm1_id}")

        # now collect stats
        stat = self.net_monitor.collect_stats()

        # print stats
        logger.info(f"stats: {stat}")

        # created vm is not under use.
        self.assertEqual(len(stat), 2)

        # create vm's
        p2 = subprocess.Popen(
            ['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100',
             '--memory size_mib=512'], cwd=VMM_REF_DIR)

        # assert vm is created or not.
        self.assertIsNotNone(p2)

        # get all vm's ids
        vm2_id = p2.pid

        logger.info(f"vm2_id: {vm2_id}")

        # allocate the vm-ids
        self.net_monitor.vm_ids.append(f"{vm1_id}")
        self.net_monitor.vm_ids.append(f"{vm2_id}")

        # now collect stats
        stat = self.net_monitor.collect_stats()

        # vm is not under use.
        self.assertEqual(len(stat), 2)

        # print stats
        logger.info(f"stats: {stat}")

        # kill all processes
        kill(vm1_id)
        kill(vm2_id)


def kill(proc_pid):
    logging.getLogger().setLevel(logging.INFO)
    logging.debug(f"kill vm-{proc_pid}")
    os.kill(proc_pid, signal.SIGTERM)


if __name__ == '__main__':
    unittest.main()

