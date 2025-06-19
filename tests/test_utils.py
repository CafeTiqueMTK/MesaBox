import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import is_valid_ip, is_valid_port

class TestUtils(unittest.TestCase):
    def test_is_valid_ip(self):
        self.assertTrue(is_valid_ip("192.168.1.1"))
        self.assertTrue(is_valid_ip("8.8.8.8"))
        self.assertFalse(is_valid_ip("256.1.1.1"))
        self.assertFalse(is_valid_ip("abc.def.ghi.jkl"))
        self.assertFalse(is_valid_ip("192.168.1"))
        self.assertFalse(is_valid_ip("192.168.1.1.1"))

    def test_is_valid_port(self):
        self.assertTrue(is_valid_port("80"))
        self.assertTrue(is_valid_port("1"))
        self.assertTrue(is_valid_port("65535"))
        self.assertFalse(is_valid_port("0"))
        self.assertFalse(is_valid_port("65536"))
        self.assertFalse(is_valid_port("-1"))
        self.assertFalse(is_valid_port("abc"))

if __name__ == "__main__":
    unittest.main()
