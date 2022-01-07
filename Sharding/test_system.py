import unittest
from record import Record
from system import System


class TestSystem(unittest.TestCase):
    def test_touch_methods(self):
        system = System()
        system.add_record(Record(1))
        system.add_record(Record(2))
        system.add_record(Record(3))
        system.sync()
        self.assertEqual(len(system.get_all()), 3)
        self.assertIsNotNone(system.get_record(1))
        self.assertIsNone(system.get_record(4))

    def test_get_databases(self):
        system = System()
        self.assertIsNotNone(system.get_main())
        self.assertIsNotNone(system.get_shard())

    def test_add_record(self):
        system = System()
        system.add_record(Record(1))
        self.assertEqual(system.get_main().records_num(), 1)
        self.assertEqual(system.get_shard().records_num(), 0)

    def test_add_record_and_sync(self):
        system = System()
        system.add_record(Record(1))
        self.assertEqual(system.get_main().records_num(), 1)
        system.sync()
        self.assertEqual(system.get_shard().records_num(), 1)

    def test_sync_twice(self):
        system = System()
        system.add_record(Record(1))
        self.assertEqual(system.get_main().records_num(), 1)
        system.sync()
        system.sync()

    def test_read_data_sync(self):
        system = System()
        system.add_record(Record(1))
        system.sync()
        self.assertIsNotNone(system.get_record(1))

    def test_read_data_no_sync(self):
        system = System()
        system.add_record(Record(1))
        self.assertIsNotNone(system.get_record(1))


class TestSystem_SetNumberOfshardics(unittest.TestCase):
    def test_1(self):
        system = System(1)
        system.get_shard(0)
        with self.assertRaises(IndexError):
            system.get_shard(1)

    def test_2(self):
        system = System(2)
        system.get_shard(0)
        system.get_shard(1)
        with self.assertRaises(IndexError):
            system.get_shard(2)

    def test_wrong_number(self):
        with self.assertRaises(ValueError):
            System(0)


class TestSystem_Stats(unittest.TestCase):
    def test_empty_1_shards(self):
        system = System(1)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0])
        
    def test_empty_2_shards(self):
        system = System(2)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0, 0])

    def test_empty_3_shards(self):
        system = System(3)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0, 0, 0])

    def test_read_1_shards(self):
        system = System(1)
        system.add_record(Record(1))
        system.sync()
        for _ in range(10):
            system.get_record(1)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [10])

    def test_read_data_once(self):
        system = System(2)
        system.add_record(Record(1))
        system.sync()
        system.get_record(1)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [1, 0])

    def test_read_data_many_times(self):
        system = System(2)
        system.add_record(Record(1))
        system.sync()
        for _ in range(10):
            system.get_record(1)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [5, 5])

    def test_break(self):
        system = System(1)
        system.add_record(Record(1))
        system.sync()
        system.get_record2(1)
        stats = system.stats()
        self.assertEqual(stats['shard2'], [1])


class TestSystem_Breaks(unittest.TestCase):
    def test_touch_methods(self):
        system = System(1)
        system.add_record(Record(1))
        system.sync()
        for _ in range(44):
            system.get_record2(1)
        for _ in range(2):
            system.get_break(1)
        stats = system.stats()
        self.assertNotEqual(stats['shard2'], [44])
        self.assertEqual(stats['break'], [2])

if __name__ == '__main__':
    unittest.main()
