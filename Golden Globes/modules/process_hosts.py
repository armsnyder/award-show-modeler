# Processes tweets to find the host names.
# This is achieved by first getting all tweets containing 'host' and then checking for capitalized bigrams within those
# tweets. Finally, the results are filtered by popularity to discern which are likely to be names of hosts.

from __future__ import division
import operator

import util
import regex


def run(db, target, limit=None):
    result = {}
    cursor = db.collection.find({'text': regex.hosts})
    i = 0
    for tweet in cursor:
        if limit and i > limit:
            break
        names = regex.name.findall(tweet['text'])
        for name in names:
            if name in result:
                result[name] += 1
            else:
                result[name] = 1
        i += 1

    # This part ensured only the most popular hits are returned
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