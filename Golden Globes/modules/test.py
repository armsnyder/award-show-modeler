#!/Users/flame/anaconda/bin/python

import sys
import os
import re
import nltk
import json

def main():
    pos_tweets = load_tweets('pos_tweets', 'positive')
    neg_tweets = load_tweets('neg_tweets', 'negative')
    tweets = []
    for (words, sentiment) in pos_tweets + neg_tweets:
        words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
        tweets.append((words_filtered, sentiment))

    word_features = get_word_features(get_words_in_tweets(tweets))

    training_set = nltk.classify.apply_features(extract_features, tweets)
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    tweet = '@iambrianprior THis gg are shit'
    print classifier.classify(extract_features(tweet.split()))


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordList):
    wordList = nltk.FreqDist(wordList)
    word_features = wordList.keys()
    return word_features


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features



nom_list = ('host', 'hosts', 'hosting')


def load_tweets(fname, sent):
    res = []
    f = open(fname)
    for line in f:
        res.append((line[:-1], sent))
    return res


def read_tweets(num):
    tweets = []
    f = open('../samples/goldenglobes2015_1_01_200000.json')
    for line in f:
        obj = json.loads(line)
        words = nltk.word_tokenize(obj['text'])
        for word in nom_list:
            if word in words:
                tweets.append(obj['text'])
                break
        num -= 1
        if num == 0:
            break
    f.close()
    for tweet in tweets:
        print tweet


if __name__ == '__main__':
    main()