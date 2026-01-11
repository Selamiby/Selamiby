"""
System Monitor testleri
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.system_monitor import SystemMonitor


class TestSystemMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = SystemMonitor(log_interval=1)
        
    def test_get_metrics(self):
        """Metrik alımı testi"""
        metrics = self.monitor.get_current_metrics()
        self.assertIsNotNone(metrics)
        self.assertIn("cpu_percent", metrics.__dict__)
        
    def test_top_processes(self):
        """Process listesi testi"""
        processes = self.monitor.get_top_processes(5)
        self.assertIsInstance(processes, list)
        self.assertLessEqual(len(processes), 5)

if __name__ == "__main__":
    unittest.main()
