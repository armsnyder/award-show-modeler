#!/Users/flame/anaconda/bin/python

# An executable file with functions that grab samples from tweet data
# This will likely not be used as a part of our final program, but it's nice for testing

import os
import sys
import json
import numpy
import unicodedata
import re


def make_random_sample(json_filename, number_of_samples):
    """generates a list of (time, tweet_text) given a json file and sample size"""

    if not os.path.isfile(json_filename):
        sys.exit(1)
    selection = sorted(get_random_selection(number_of_samples, 1754153))
    sample = []
    with open(json_filename, 'r') as json_file:
        i = 1
        for line in json_file:
            if not selection:
                break
            if i == selection[0]:
                selection.pop(0)
                tweet = json.loads(line)
                sample.append((tweet['created_at'], tweet['text']))
            i += 1
    return sample


def make_verified_sample(json_filename, number_of_samples):
    """generates a list of (time, tweet_text) from only verified twitter users given a json file and sample size"""

    if not os.path.isfile(json_filename):
        sys.exit(1)
    tweets = []
    with open(json_filename, 'r') as json_file:
        for line in json_file:
            tweet = json.loads(line)
            if tweet['user']['verified']:
                tweets.append((tweet['created_at'], tweet['text'], tweet['user']['screen_name']))
    selection = sorted(get_random_selection(number_of_samples, 38111))
    print len(tweets)
    print len(selection)
    sample = []
    i = 1
    for tweet in tweets:
        if not len(selection):
            break
        if i == selection[0]:
            selection.pop(0)
            sample.append(tweet)
        i += 1
    return sample


def print_sample(sample):
    """prints a sample of tweets"""

    number_of_samples = len(sample)
    sample_type = len(sample[0])
    f = open('sample_of_'+str(number_of_samples)+'.txt', 'w')
    i = 0
    if sample_type == 2:
        for time, text in sample:
            u_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
            f_text = re.sub('\s+', ' ', u_text)
            if f_text:
                i += 1
            f.write(time+'   '+f_text+'\n')
    if sample_type == 3:
        for time, text, username in sample:
            u_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
            f_text = re.sub('\s+', ' ', u_text)
            if f_text:
                i += 1
            f.write(time+'  '+username+':  '+f_text+'\n')
    return str(i) + 'lines wrote'


def get_random_selection(num, total_tweets):
    """generates a list of random numbers from 1 to 1754153 given a sample size"""

    return numpy.random.random_integers(1, total_tweets, num)


def print_verified(json_filename, number_of_samples):
    """prints random verified tweets json file and sample size"""

    return print_sample(make_verified_sample(json_filename, number_of_samples))


def print_random(json_filename, number_of_samples):
    """prints random tweets, given a json file and sample size"""
    return print_sample(make_random_sample(json_filename, number_of_samples))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'usage: [random | verified] json_file sample_size'
    if sys.argv[1] == 'random':
        print_random(sys.argv[2], int(sys.argv[3]))
    if sys.argv[1] == 'verified':
        print_verified(sys.argv[2], int(sys.argv[3]))