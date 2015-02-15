# Processes tweets to find the winners
# TODO: Write a function that takes our bins and collapses them by looking up twitter handles, hashtags, etc
# TODO: Write a function that tales the collapsed bins and uses statistical analysis to find the real winners
    # TODO: (possibly using hamming distance)


import nltk
import datetime
from dateutil import tz

import regex
from util import vprint
import util


def run(db, target, event):
    event.wait()  # Wait for start_time to be set
    vprint('Received start time. Processing winners...')
    cursor = db.collection.find({"text": regex.winners, 'retweeted_status': {'$exists': False}})
    for tweet in cursor:
        tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')\
            .replace(tzinfo=tz.gettz('UTC'))
        if weed_out(tweet, target, tweet_time):
            continue
        parsed_tweet = None
        model_num = 0
        for winner_model in regex.winner_models:
            match = winner_model.search(tweet['text'])
            if match:
                parsed_tweet = match
                break
            model_num += 1
        if not parsed_tweet:
            continue
        winner = parsed_tweet.group(1)
        award = parsed_tweet.group(2)
        if winner in target.winner_bins.keys():
            target.winner_bins[winner].append((award, tweet_time))
        else:
            target.winner_bins[winner] = [(award, tweet_time)]


def weed_out(tweet, target, tweet_time):
    # Check for subjunctive
    if regex.subjunctive.search(tweet['text']):
        return True
    # Check if tweet occurs before event starts
    if tweet_time < target.start_time:
        return True
    return False