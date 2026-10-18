import unittest
from datetime import datetime
from export_index_chaufferie import extraire

class TestExport(unittest.TestCase):
    def test_index(self):
        date, index = extraire("vendredi 16 octobre 2026 00:00:00\t1234510,0000")
        self.assertEqual(date, datetime(2026, 10, 16))
        self.assertEqual(index, 1234510.0)

    def test_date_invalide(self):
        with self.assertRaises(ValueError):
            extraire("vendredi 32 octobre 2026 00:00:00\t12,0")

    def test_index_invalide(self):
        with self.assertRaises(ValueError):
            extraire("vendredi 16 octobre 2026 00:00:00\tABC")

    def test_espaces(self):
        date, index = extraire("vendredi 16 octobre 2026 00:00:00    1234510,0000")
        self.assertEqual(index, 1234510.0)

    def test_point_virgule(self):
        date, index = extraire("vendredi 16 octobre 2026 00:00:00;1234510,0000")
        self.assertEqual(index, 1234510.0)
