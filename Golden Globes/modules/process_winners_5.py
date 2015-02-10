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
        with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch2.txt', 'w') as noms:
            for tweet in cursor:
                tweet_category = categorize_tweet(tweet, target)
                if tweet_category == 3:
                    continue
                elif tweet_category == 1:
                    t = nltk.word_tokenize(tweet['text'])
                    if t[0] == 'RT':
                        continue
                    t_pr = ''
                    for b in t:
                        t_pr += '(' + b + ') '
                    # p_tweet = nltk.word_tokenize(tweet['text'])
                    wins.write(t_pr.encode('utf8')+'\n')
                else:
                    t = nltk.word_tokenize(tweet['text'])
                    if t[0] == 'RT':
                        continue
                    t_pr = ''
                    for b in t:
                        t_pr += '(' + b + ') '
                    # p_tweet = nltk.word_tokenize(tweet['text'])
                    noms.write(t_pr.encode('utf8')+'\n')


def categorize_tweet(tweet, target):
    # Check if tweet occurs before event starts
    if regex.subjunctive.search(tweet['text']):
        return 2
    tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')\
        .replace(tzinfo=tz.gettz('UTC'))
    if tweet_time < target.start_time:
        return 3
    return 1