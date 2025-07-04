"""
Unit tests for utility functions
"""

import unittest
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.utils import validate_target, setup_temp_directory, format_duration

class TestUtils(unittest.TestCase):
    
    def test_validate_target_ip(self):
        """Test IP address validation"""
        self.assertTrue(validate_target('192.168.1.1'))
        self.assertTrue(validate_target('10.0.0.1'))
        self.assertFalse(validate_target('256.1.1.1'))
        self.assertFalse(validate_target('192.168.1'))
    
    def test_validate_target_cidr(self):
        """Test CIDR range validation"""
        self.assertTrue(validate_target('192.168.1.0/24'))
        self.assertTrue(validate_target('10.0.0.0/8'))
        self.assertFalse(validate_target('192.168.1.0/33'))
        self.assertFalse(validate_target('192.168.1.0/'))
    
    def test_validate_target_domain(self):
        """Test domain name validation"""
        self.assertTrue(validate_target('example.com'))
        self.assertTrue(validate_target('sub.example.com'))
        self.assertTrue(validate_target('test-site.co.uk'))
        self.assertFalse(validate_target('invalid..domain'))
        self.assertFalse(validate_target('.example.com'))
    
    def test_setup_temp_directory(self):
        """Test temporary directory creation"""
        temp_dir = setup_temp_directory()
        self.assertTrue(os.path.exists(temp_dir))
        self.assertTrue(os.path.isdir(temp_dir))
        # Cleanup
        os.rmdir(temp_dir)
    
    def test_format_duration(self):
        """Test duration formatting"""
        self.assertEqual(format_duration(30), "30.0 seconds")
        self.assertEqual(format_duration(90), "1.5 minutes")
        self.assertEqual(format_duration(3660), "1.0 hours")

if __name__ == '__main__':
    unittest.main()
