import unittest
from record import *
from db import *


class TestDatabase(unittest.TestCase):
    def test_break(self):
        db = Database()
        self.assertTrue(db.get_break)

    def test_no_break(self):
        db = Database()
        self.assertFalse(db.get_no_break())
    
    def test_empty(self):
        db = Database()
        self.assertEqual(db.records_num(), 0)

    def test_add_records(self):
        db = Database()
        db.add_record(Record(1))
        db.add_record(Record(2))
        self.assertEqual(db.records_num(), 2)

    def test_delete_records(self):
        db = Database()
        db.add_record(Record(1))
        db.add_record(Record(2))
        db.delete_record(Record(2))
        self.assertNotEqual(db.records_num(), 2)

    def test_add_same_record_twice(self):
        db = Database()
        db.add_record(Record(1))
        with self.assertRaises(ValueError):
            db.add_record(Record(1))

    def test_get_record_exists(self):
        db = Database()
        db.add_record(Record(99))
        self.assertIsNotNone(db.get_record(99))

    def test_get_record_not_exists(self):
        db = Database()
        db.add_record(Record(1))
        self.assertIsNone(db.get_record(2))

    def test_get_all(self):
        db = Database()
        n = 34545
        for i in range(1, n + 1):
            db.add_record(Record(i))
        self.assertEqual(len(db.get_all()), n)
    
if __name__ == '__main__':
    unittest.main()
