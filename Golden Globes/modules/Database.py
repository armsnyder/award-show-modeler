# Database object, used for managing connections, loading tweets
# Don't worry too much about understanding this one. Just look at how the Database object is interfaced with in the
# already-written modules, often referred to as 'db'

import pymongo
import os
import re
import json

from util import vprint
from util import warning
from ProgressBar import ProgressBar


class Database:

    def __init__(self, db, collection, force_reload):
        self.conn = None  # stores the mongo client object
        self.db = None  # stores the database we connect to
        self.collection = None  # stores the tweet table
        self.i = 0  # used as a counter for multithreaded write operation
        self.collection_name = self.format_collection_name(collection)
        self.json_name = self.format_json_name(collection)
        self.connect()
        self.access(self.collection_name)
        self.load_collection(force_reload)
        return

    def __del__(self):
        self.conn.disconnect()

    def connect(self):
        """establishes connection with mongoDB"""
        try:
            self.conn = pymongo.MongoClient()
            vprint("Connected to MongoDB")
        except pymongo.errors.ConnectionFailure, e:
            warning("Could not connect to MongoDB: %s" % e, exit=True)
        return

    def access(self, db_name):
        """connects to a mongoDB database"""
        if db_name in self.conn.database_names():
            vprint("Connecting to existing %s database" % db_name)
        else:
            vprint("Initializing new %s database" % db_name)
        self.db = self.conn[db_name]
        return

    def load_collection(self, force_reload):
        if self.collection_name not in self.db.collection_names():
            self.write_tweets()
        else:
            self.collection = self.db[self.collection_name]
            if force_reload:
                vprint('Deleting collection')
                self.collection.drop()
                self.write_tweets()
        return

    def write_tweets(self):
        """loads tweets from a JSON file and writes them to the database"""
        self.collection = self.db[self.collection_name]
        vprint('Preparing to load tweets...')
        if not os.path.isfile(self.json_name):
            warning('The requested file does not exist: %s' % self.json_name, exit=True)
        total_tweets = sum(1 for line in open(self.json_name, 'r'))
        bar = ProgressBar('Loading Tweets', total_tweets)
        with open(self.json_name, 'r') as f:
            i = 0
            for tweet in f:
                tweet_json = json.loads(tweet)
                data = Database.load_tweet_json(tweet_json)
                self.collection.insert(data)
                i += 1
                if not i % 1000:
                    bar.set_progress(i)
        bar.end_progress()
        vprint('Finished writing tweets!')
        return

    @staticmethod
    def load_tweet_json(tweet):
        """returns important fields from tweet object
        once we get further we may specify only specific fields to load"""
        return tweet

    @staticmethod
    def format_collection_name(text):
        """formats a JSON filename as a collection name"""
        result = text
        match = re.search(r'(\w+).json', text)
        if match:
            result = match.group(1)
        return result

    @staticmethod
    def format_json_name(text):
        """formats a collection name as a JSON filename"""
        result = text
        match = re.search(r'\w+.json', text)
        if not match:
            result += '.json'
        return result