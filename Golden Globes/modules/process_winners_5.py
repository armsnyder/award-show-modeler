# Processes tweets to find the winners

import re
import nltk
import datetime
from dateutil import tz

pattern_nom = re.compile(r'\bnomin(ee|at)', re.I)
pattern_congratulatory = re.compile(r'congratulatory', re.I)
pattern_good_luck = re.compile(r'good luck', re.I)


def run(db, target, event):
    event.wait()
    pattern = re.compile(r'congrat', re.I)
    cursor = db.collection.find({"text": pattern})
    with open('/Users/flame/Desktop/output.txt', 'w') as f:
        for tweet in cursor:
            if weed_out(tweet, target):
                continue
            t = nltk.word_tokenize(tweet['text'])
            t_pr = ''
            for b in t:
                t_pr += '(' + b + ') '
            # p_tweet = nltk.word_tokenize(tweet['text'])
            f.write(t_pr.encode('utf8')+'\n')


def weed_out(tweet, target):
    # Check if tweet occurs before event starts
    tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')\
        .replace(tzinfo=tz.gettz('UTC'))
    if tweet_time < target.start_time:
        return True
    # Check if tweet mentions nominee
    if pattern_nom.search(tweet['text']):
        return True
    # Check if tweet misuses congratulatory
    if pattern_congratulatory.search(tweet['text']):
        return True
    # Check if tweet is wishful
    if pattern_good_luck.search(tweet['text']):
        return True
    return False