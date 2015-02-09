# Processes tweets to find the winners

import re


def run(db, target, event, limit=None):
    event.wait()
    result = {}
    pattern = re.compile(r'best', re.I)
    useful_tweets = db.collection.find({
        "text": pattern,
        "created_at": {
            "$gt": target.start_time,
        }

    })
    i = 0
    for tweet in useful_tweets:
        if limit and i > limit:
            break
        #TODO: Some shit
    return