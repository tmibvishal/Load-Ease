import unittest
import subprocess
from Monitoring.config import VMM_REF_DIR

from Monitoring.memory_monitoring import MemoryMonitor
  
class SimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        p = subprocess.Popen(['./target/debug/vmm-reference', '--kernel path=./bzimage-hello-busybox', '--net tap=vmtap100', '--memory size_mib=512'], cwd=VMM_REF_DIR)
        # Find this new vm process id
        
        mem_monitor = MemoryMonitor()

    def test(self):        
        self.assertTrue(True)
  
if __name__ == '__main__':
    unittest.main()