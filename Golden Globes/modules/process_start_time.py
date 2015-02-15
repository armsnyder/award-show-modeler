# Processes tweets to find event start time.
# Currently way too slow and should definitely be optimized.
# Works by pulling tweets that match a regex, then with each tweet, creating a datetime that refers to the tweet's
# proclaimed start time, also using some timezone conversions.
# It works. It's done.

import datetime
from dateutil import tz

import regex
import util


def run(db, target, event, limit=None):
    result = {}
    useful_tweets = db.collection.find({"text": regex.time})
    utc_zone = tz.gettz('UTC')
    i = 0
    for tweet in useful_tweets:
        if limit and i > limit:
            break
        tweet_text = tweet['text']
        match = regex.time.search(tweet_text)
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
        i += 1
    if result:
        target.start_time = sorted(result, key=result.get, reverse=True)[0]
    else:
        util.warning('Failed to determine event start time')
    event.set()  # Tells other threads that rely on a start time that it has been set