# Database object, used for managing connections, loading tweets

import pymongo
from util import vprint


class Database:

    def __init__(self, db='gg'):
        self.conn = 0
        self.db = 0

        self.connect()
        self.access(db)
        return

    def connect(self):
        try:
            self.conn = pymongo.MongoClient()
            vprint("Connected to MongoDB")
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
            del self
        return

    def access(self, db_name):
        if db_name in self.conn.database_names():
            print "Connecting to existing %s database" % db_name
        else:
            print "Database %s found" % db_name
            print "Initializing new %s database" % db_name
        self.db = self.conn[db_name]
        return

    def load(self, collection):
        if collection not in self.db.collection_names():
            self.load_tweets(collection)
        return

    def load_tweets(self, filename):
        return