# Processes tweets to find event start time.
# Currently way too slow and should definitely be optimized.
# Works by pulling tweets that match a regex, then with each tweet, creating a datetime that refers to the tweet's
# proclaimed start time, also using some timezone conversions.

import re
import datetime
from dateutil import tz
from util import vprint


def run(db, target):
    vprint('Processing start time...')
    result = {}
    pattern = re.compile(optional_space(target.show_name) + r'.*at (\d+):?\d* *([ap]m) ?(\w\w?\w?T)', re.I)
    useful_tweets = db.collection.find({"text": pattern})
    utc_zone = tz.gettz('UTC')
    for tweet in useful_tweets:
        tweet_text = tweet['text']
        match = pattern.search(tweet_text)
        from_zone = tz.gettz(match.group(3))
        if not from_zone:
            continue
        hour = int(match.group(1))
        if match.group(2) == 'pm':
            hour += 12
        tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')\
            .replace(tzinfo=utc_zone).astimezone(from_zone)
        res_time = datetime.datetime(tweet_time.year, tweet_time.month, tweet_time.day, hour, tzinfo=from_zone)\
            .astimezone(utc_zone)
        if res_time in result:
            result[res_time] += 1
        else:
            result[res_time] = 1
    target.start_time = sorted(result, key=result.get, reverse=True)[0]
    vprint('Processing start time finished')
    return


def optional_space(text):
    return text.replace(' ', ' ?')