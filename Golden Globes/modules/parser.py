import sys
import os
import json
from util import warning


def load_tweets(filename):
    if not os.path.isfile(filename):
        warning("Not a valid filename: "+filename)
        sys.exit(1)
    with open(filename, 'r') as json_file:
        for line in json_file:
            parse_tweet(json.loads(line))
    return


def parse_tweet(json_tweet):
    return