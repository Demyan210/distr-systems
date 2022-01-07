"""System with sharding."""
from db import Database


class System:
    """System with sharding."""
    def __init__(self, shards_num=1):
        if shards_num < 1:
            raise ValueError("shards_num must be positive")

        self.__main = Database()
        self.__shards = []
        self.__shards2 = []
        self.__breaks = []
        for _ in range(shards_num):
            self.__shards.append(Database())
            self.__shards2.append(Database())
            self.__breaks.append(Database())

        self.__stats = {
            'main': 0,
            'shard': [],
            'shard2': [],
            'break': [],
        }
        for _ in range(shards_num):
            self.__stats['shard'].append(0)
            self.__stats['shard2'].append(0)
            self.__stats['break'].append(0)
        self.__ind = 0

    def get_main(self):
        """Return main DB."""
        return self.__main

    def get_shard(self, ind=0):
        """Return replicated DB."""
        return self.__shards[ind]

    def sync(self):
        """Synchronize system."""
        for shard in self.__shards:
            _sync(self.__main, shard)

    def add_record(self, rec):
        """Add record to database."""
        return self.__main.add_record(rec)

    def get_record(self, record_id):
        """Get record by ID."""
        rec = self.__shards[self.__ind].get_record(record_id)
        self.__stats['shard'][self.__ind] += 1
        self.__update_ind()
        if rec:
            return rec
        return self.__main.get_record(record_id)

    def get_all(self):
        """Return all records."""
        res = self.__shards[self.__ind].get_all()
        self.__stats['shard'][self.__ind] += 1
        self.__update_ind()
        return res

    def stats(self):
        """Return statistics of readings."""
        return self.__stats

    def __update_ind(self):
        self.__ind = (self.__ind + 1) % len(self.__shards)
        
    def get_record2(self, record_id):
        """Get Working Database."""
        rec = self.__shards2[self.__ind].get_record(record_id)
        self.__stats['shard2'][self.__ind] += 1
        self.__update_ind()
        if rec:
            return rec
        return self.__main.get_record(record_id)

    def get_break(self, record_id):
        rec = self.__shards2[self.__ind].get_record(record_id)
        self.__stats['shard2'][self.__ind] -= 1
        self.__stats['break'][self.__ind] += 1
        self.__update_ind()
        if rec:
            return rec
        return self.__main.get_record(record_id)


def _sync(src, dst):
    records = src.get_all()
    for rec_id, rec in records.items():
        if not dst.get_record(rec_id):
            dst.add_record(rec)
