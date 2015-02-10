# Processes tweets to find the winners

import nltk
import datetime
from dateutil import tz
import regex


def run(db, target, event):
    event.wait()
    print target.start_time
    cursor = db.collection.find({"text": regex.winners})
    with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch1.txt', 'w') as wins:
        for tweet in cursor:
            if weed_out(tweet, target):
                continue
            t = nltk.word_tokenize(tweet['text'])
            if t[0] == 'RT':
                continue
            t_pr = ''
            for b in t:
                t_pr += '(' + b + ') '
            # p_tweet = nltk.word_tokenize(tweet['text'])
            wins.write(t_pr.encode('utf8')+'\n')


def weed_out(tweet, target):
    # Check for subjunctive
    if regex.subjunctive.search(tweet['text']):
        return True
    # Check if tweet occurs before event starts
    tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')\
    .replace(tzinfo=tz.gettz('UTC'))
    if tweet_time < target.start_time:
        return True
    return False