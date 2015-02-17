# Processes tweets to find the best/worst dressed.
# TODO: Find a way to display pictures (URL-based?)
# Tried the above. Turns out that the media_url is not included in this JSON,
# so trying to just find most popular names instead
# This wouldn't have been great without a GUI anyway.
# TODO: Figure out the best popularity ratio. Spit out a top 5 list in Result.py?
# for top k results, run edit distance on each pair to get rid of misspellings.

from __future__ import division
import operator
import nltk


import regex
from util import vprint
import util
import urllib2


def run(db, target):
    vprint('Processing Best Dressed...')
    best = {}
    tweets = db.collection.find({'text': regex.best_dressed})
    for tweet in tweets:
        text = tweet['text']
        tokens = nltk.word_tokenize(text)
        bg = nltk.bigrams(tokens)
        for name in bg:
            if name[0] in util.bad_names or name[1] in util.bad_names:
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


# everything below here is a failed attempt

# def read_best_dressed(db, target):
#     tweets = db.collection.find({'text': regex.best_dressed})
#     # Only read in tweets that contain images
#     for tweet in tweets:
#         if tweet['entities']['media']['media_url']:
#             text = tweet['text']
#             url = tweet['entities']['media']['media_url']
#         else:
#             continue
#     together = [text, url]
#     return together



# def run(db, target):
#     vprint('Processing Best Dressed...')
#     tweets = db.collection.find({'text': regex.best_dressed})
#     text = [tweet['text'] for tweet in tweets]
#     urls = [(tweet['entities']['media_url'] if len(tweet['entities']['media_url']) >= 1 else None) for tweet in tweets]
#     text_url = [text, urls]
#     target.best_dressed = text_url[1]


# def run(db, target):
#     vprint('Processing Best Dressed...')
#     best_dressed = {}
#     cursor = db.collection.find({'text': regex.best_dressed})
#     for tweet in cursor.entities.setdefault('media', []):
#         best_dressed.append(tweet['media_url'])
#


# def run(db, target):
#     vprint('Processing Red Carpet...')
#     result = {}
#     cursor = db.collection.find({'text': regex.best_dressed})
#     i = 0
#     for tweet in cursor:
#         if limit and i > limit:
#             break
#         tweet_text = tweet['text']
#         tweet_url = tweet['entities']['media_url']
#         tokens = nltk.word_tokenize(tweet_text)
#         bgs = nltk.bigrams(tokens)
#         for name in bgs:
#             if name[0][0].isupper() and name[1][0].isupper():
#                 if name in result:
#                     result[name] += 1
#                 else:
#                     result[name] = 1
#         i += 1
