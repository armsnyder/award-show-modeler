# Processes tweets to find the host names.
# This is achieved by first getting all tweets containing 'host' and then checking for capitalized bigrams within those
# tweets. Finally, the results are filtered by popularity to discern which are likely to be names of hosts.

from __future__ import division
import nltk
import operator
import util


def run(db, target, limit=None):
    result = {}
    useful_tweets = db.find('host')
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

    most_popular = None
    for name, popularity in sorted(result.items(), key=operator.itemgetter(1), reverse=True):
        if not most_popular:
            most_popular = popularity
        percent_popularity = popularity / most_popular
        if percent_popularity > util.host_threshold:
            target.hosts.append(name)
        else:
            break
    return