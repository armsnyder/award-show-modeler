# Processes tweets to find the winners

from __future__ import division
import re
import nltk
import operator
import util


def run(db, target, event, limit=None):
    # TODO: Threading (Flame)
    # cursor = db.find('Best')
    # for tweet in cursor:
    #     print tweet['text']
    # sys.close()
    # event.wait()
    result = {}
    pattern = re.compile(r'^(?!.*best).*(w[io]n[ns\s]+|congrat.+|goes to).*$', re.I)
    useful_tweets = db.collection.find({
        "text": pattern

        # TODO: Add starting time
        # "created_at": {
        #     "$gt": target.start_time,
        # }

    })
    i = 0
    for tweet in useful_tweets:
        if limit and i > limit:
            break
        tweet_text = tweet['text']
        tokens = nltk.word_tokenize(tweet_text)
        bgs = nltk.bigrams(tokens)
        for name in bgs:
            if name[0][0].isupper() and name[1][0].isupper():
                if name in result:
                    result[name] += 1
                else:
                    result[name] = 1
        i += 1
        # TODO: Process for result
    return