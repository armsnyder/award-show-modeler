# Processes tweets to find event start time
# Works by pulling tweets that match a regex, then with each tweet, creating a datetime that refers to the tweet's
# proclaimed start time, also using some timezone conversions.

import datetime
from dateutil import tz
import calendar

import regex
import util


def run(db, target, event, event_wait, limit=None):
    event_wait.wait()
    result = {}
    useful_tweets = db.collection.find({'text': regex.time})
    utc_zone = tz.gettz('UTC')
    i = 0
    for tweet in useful_tweets:
        if limit and i > limit:
            break
        tweet_text = tweet['text']
        print tweet_text
        match = regex.time.search(tweet_text)
        from_zone = tz.gettz(match.group(3))
        if not from_zone:
            continue
        hour = int(match.group(1))
        if match.group(2) == 'pm':
            hour += 12
        tweet_time = util.timestamp_to_datetime(int(tweet['timestamp_ms']))\
            .replace(tzinfo=utc_zone).astimezone(from_zone)
        res_time = datetime.datetime(tweet_time.year, tweet_time.month, tweet_time.day, hour, tzinfo=from_zone)\
            .astimezone(utc_zone)
        res_timestamp = calendar.timegm(res_time.utctimetuple()) * 1000
        if res_timestamp in result:
            result[res_timestamp] += 1
        else:
            result[res_timestamp] = 1
        i += 1
    if result:
        target.start_time = sorted(result, key=result.get, reverse=True)[0]
    else:
        util.warning('Failed to determine event start time', exit=True)
    event.set()  # Tells other threads that rely on a start time that it has been set