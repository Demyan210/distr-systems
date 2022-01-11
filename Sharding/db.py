"""Sharding example."""


class Database:
    """Database prototype."""
    def __init__(self):
        self.__records = {}

    def records_num(self):
        """Number of records."""
        return len(self.__records)

    def add_record(self, r):
        """Add record to database."""
        if r.get_id() in self.__records:
            raise ValueError("Duplicated ID")
        self.__records[r.get_id()] = r

    def delete_record(self, r):
        """Add record to database."""
        del self.__records[r.get_id()]

    def get_record(self, record_id):
        """Get record by ID."""
        try:
            return self.__records[record_id]
        except KeyError:
            return None

    def get_all(self):
        """Return all records."""
        return self.__records

    def get_break(self):
        """Broken Database."""
        self.__break = True
        
    def get_no_break(self):
        """Working Database."""
        #TODO break broken
        self.__break = False
