import json
import os
"""Replication example."""


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

    def get_record(self, record_id):
        """Get record by ID."""
        try:
            return self.__records[record_id]
        except KeyError:
            return None

    def get_all(self):
        """Return all records."""
        return self.__records


class FoobarDB(object):
    def __init__(self, location):
        self.locations = {}
        self.load(self.location)

    def load(self , location):
       if os.path.exists(location):
           self._load()
       else:
            self.db = {}
       return True
        
    def _load(self):
        """Open database"""
        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        """Saving database"""
        try:
            json.dump(self.db , open(self.location, "w+"))
            return True
        except:
            return False

    def set(self , key , value):
        """Adding data in database"""
        try:
            self.db[str(key)] = value
            self.dumpdb()
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False

    def get(self , key):
        """Database browsing"""
        try:
            return self.db[key]
        except KeyError:
            print("No Value Can Be Found for " + str(key))
            return False

    def delete(self , key):
        """Delete key"""
        if not key in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True
    
    def resetdb(self):
        """Reset database"""
        self.db={}
        self.dumpdb()
        return True

