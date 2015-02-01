import sys
import os
import ujson
import nltk
from util import warning


def parse_tweets(filename):
    if valid_file(filename):
        ujson.load(filename)
    else:
        warning("Not a valid filename: "+filename)
        sys.exit(1)
    sys.exit(0)
    return


def valid_file(filename):
    return os.path.isfile(filename)