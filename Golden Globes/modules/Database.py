# Database object, used for managing connections, loading tweets

# TODO: Add methods for reading tweets from database

import pymongo
import os
import re
import json

from util import vprint
from util import warning


class Database:

    def __init__(self, db, collection):
        self.conn = 0
        self.db = 0
        self.collection = 0
        self.collection_name = self.format_collection_name(collection)
        self.json_name = self.format_json_name(collection)
        self.connect()
        self.access(db)
        self.load_collection()
        return

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
            vprint("Database %s found" % db_name)
            vprint("Initializing new %s database" % db_name)
        self.db = self.conn[db_name]
        return

    def load_collection(self):
        if self.collection_name not in self.db.collection_names():
            self.write_tweets()
        return

    def write_tweets(self):
        """loads tweets from a JSON file and writes them to the database"""
        self.collection = self.db[self.collection_name]
        vprint('Loading tweets into database...')
        if not os.path.isfile(self.json_name):
            warning('The requested file does not exist: %s' % self.json_name, exit=True)
        f = open(self.json_name, 'r')
        for tweet in f:
            tweet_json = json.loads(tweet)
            data = Database.load_tweet_json(tweet_json)
            self.collection.insert(data)
        vprint('Tweets loaded successfully')
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