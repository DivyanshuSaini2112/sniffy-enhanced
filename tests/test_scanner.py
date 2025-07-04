"""
Unit tests for the main scanner functionality
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.scanner import SniffyScanner
from core.config import Config
from core.logger import Logger

class TestSniffyScanner(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.logger = Logger()
        self.scanner = SniffyScanner(self.config, self.logger)
    
    def test_scanner_initialization(self):
        """Test scanner initializes correctly"""
        self.assertIsNotNone(self.scanner.config)
        self.assertIsNotNone(self.scanner.logger)
        self.assertFalse(self.scanner.stealth)
        self.assertFalse(self.scanner.deep_scan)
    
    @patch('core.scanner.NetworkScanner')
    def test_scan_target(self, mock_network_scanner):
        """Test scanning a single target"""
        # Mock network scanner
        mock_network_scanner.return_value.scan.return_value = {
            'open_ports': [{'port': 80, 'service': 'http'}]
        }
        
        result = self.scanner.scan_target('127.0.0.1')
        
        self.assertIsInstance(result, dict)
        self.assertIn('network', result)
        self.assertIn('scan_info', result)
    
    def test_get_web_ports(self):
        """Test web port extraction"""
        open_ports = [
            {'port': 80, 'service': 'http'},
            {'port': 443, 'service': 'https'},
            {'port': 22, 'service': 'ssh'},
            {'port': 8080, 'service': 'http-proxy'}
        ]
        
        web_ports = self.scanner._get_web_ports(open_ports)
        
        self.assertEqual(len(web_ports), 3)
        self.assertIn(80, web_ports)
        self.assertIn(443, web_ports)
        self.assertIn(8080, web_ports)
        self.assertNotIn(22, web_ports)

if __name__ == '__main__':
    unittest.main()
