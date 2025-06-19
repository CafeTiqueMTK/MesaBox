import unittest
from src.bssid_scanner import load_bssid_list, BSSID_JSON_PATH
import json
import os

class TestBSSIDScanner(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"bssid": "00:11:22:33:44:55", "ssid": "TestNet"},
            {"bssid": "66:77:88:99:AA:BB", "ssid": "AnotherNet"}
        ]
        with open(BSSID_JSON_PATH, "w") as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        if os.path.exists(BSSID_JSON_PATH):
            os.remove(BSSID_JSON_PATH)

    def test_load_bssid_list(self):
        result = load_bssid_list()
        self.assertEqual(result, self.test_data)

if __name__ == "__main__":
    unittest.main()
