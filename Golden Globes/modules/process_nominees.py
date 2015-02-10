# Processes tweets to find the nominees

import regex
import re
import nltk
import datetime
from dateutil import tz
import operator
import imdb
imdb_access = imdb.IMDb()


def run(db, target):
    names = {}
    i = 0
    cursor = db.collection.find({"text": regex.subjunctive})
# with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch1.txt', 'w') as f:
    for tweet in cursor:
        n = regex.name.match(tweet['text'])
        if n:
            if n.group() in names:
                names[n.group()] += 1
            elif not weed_out(n.group(), target):
                names[n.group()] = 1
        else:
            continue
    print sorted(names.items(), key=operator.itemgetter(1), reverse=True)

# TODO: weed out winners, assign categories


def weed_out(name, target):
    if name in target.hosts:
        return True
    if name in target.winning_people:
        return True
    return False