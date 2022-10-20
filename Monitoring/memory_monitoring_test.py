import unittest

from Monitoring.memory_monitoring import MemoryMonitor
  
class SimpleTest(unittest.TestCase):

    def setUp(self) -> None:
        mem_monitor = MemoryMonitor()
    def test(self):        
        self.assertTrue(True)
  
if __name__ == '__main__':
    unittest.main()