import unittest
from mesabox.scanner import parse_ports

class TestScanner(unittest.TestCase):
    def test_parse_ports(self):
        self.assertEqual(parse_ports("22,80,443"), [22, 80, 443])
        self.assertEqual(parse_ports("20-22"), [20, 21, 22])
        self.assertEqual(parse_ports("20-22,80"), [20, 21, 22, 80])
        self.assertEqual(parse_ports("abc"), [])
        self.assertEqual(parse_ports("70000"), [])
        self.assertEqual(parse_ports("1-3,abc,65536"), [1, 2, 3])

if __name__ == "__main__":
    unittest.main()
