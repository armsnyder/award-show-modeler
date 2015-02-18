# Processes tweets to find event name

import regex
import util


def run(db, target, event, limit=None):
    event_names = {}
    useful_tweets = db.collection.find({})
    i = 0
    for tweet in useful_tweets:
        if limit and i > limit:
            break
        tweet_text = tweet['text']
        match = regex.hashtag.findall(tweet_text)
        for tag in match:
            tag = util.camel_to_space(tag)
            if tag in event_names:
                event_names[tag] += 1
            else:
                event_names[tag] = 1
        i += 1
    if event_names:
        target.event_name = sorted(event_names, key=event_names.get, reverse=True)[0]
        regex.update_name_regex(target.event_name)
        util.update_common_words(target.event_name)
    else:
        util.warning('Failed to determine event name', exit=True)
    event.set()  # Tells other threads that rely on an event name that it has been set