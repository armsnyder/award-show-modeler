# Processes tweets to find the worst dressed

from __future__ import division
import operator
import nltk

import regex
import util


def run(db, target, event):
    event.wait()
    worst = {}
    tweets = db.collection.find({'text': regex.worst_dressed})
    for tweet in tweets:
        text = tweet['text']
        tokens = nltk.word_tokenize(text)
        bg = nltk.bigrams(tokens)
        for name in bg:
            if name[0].lower() in util.common_words or name[1].lower() in util.common_words:
                continue
            if name[0][0].isupper() and name[1][0].isupper():
                if name in worst:
                    worst[name] += 1
                else:
                    worst[name] = 1
    most_popular = None
    sorted_worst = sorted(worst.items(), key=operator.itemgetter(1), reverse=True)
    for name, popularity in sorted_worst:
        if not most_popular:
            most_popular = popularity
        percent_popularity = popularity / most_popular
        if percent_popularity > 0.5:
            typo = False
            for n in target.worst_dressed:
                if nltk.metrics.edit_distance(n, name) < 4:
                    typo = True
            if not typo:
                target.worst_dressed.append(name)
        else:
            break
    return
