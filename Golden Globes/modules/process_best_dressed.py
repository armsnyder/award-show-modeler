# Processes tweets to find the best dressed

from __future__ import division
import operator
import nltk

import regex
import util


def run(db, target, event):
    event.wait()
    best = {}
    tweets = db.collection.find({'text': regex.best_dressed})
    for tweet in tweets:
        text = tweet['text']
        tokens = nltk.word_tokenize(text)
        bg = nltk.bigrams(tokens)
        for name in bg:
            if name[0].lower() in util.common_words or name[1].lower() in util.common_words:
                continue
            if name[0][0].isupper() and name[1][0].isupper():
                if name in best:
                    best[name] += 1
                else:
                    best[name] = 1
    most_popular = None
    sorted_best = sorted(best.items(), key=operator.itemgetter(1), reverse=True)
    for name, popularity in sorted_best:
        if not most_popular:
            most_popular = popularity
        percent_popularity = popularity / most_popular
        if percent_popularity > 0.5:
            target.best_dressed.append(name)
        else:
            break
    return
