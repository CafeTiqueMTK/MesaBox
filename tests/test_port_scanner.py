import unittest
from src.port_scanner import parse_ports

class TestPortScanner(unittest.TestCase):
    def test_parse_ports_single(self):
        self.assertEqual(parse_ports("80"), [80])
        self.assertEqual(parse_ports("22,80,443"), [22, 80, 443])

    def test_parse_ports_range(self):
        self.assertEqual(parse_ports("20-22"), [20, 21, 22])
        self.assertEqual(parse_ports("20-22,80"), [20, 21, 22, 80])

    def test_parse_ports_invalid(self):
        self.assertEqual(parse_ports("abc"), [])
        self.assertEqual(parse_ports("70000"), [])
        self.assertEqual(parse_ports("1-3,abc,65536"), [1, 2, 3])

if __name__ == "__main__":
    unittest.main()
