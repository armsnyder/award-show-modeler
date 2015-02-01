#!~/anaconda/bin/
# Golden Globes Natural Language Processor
# by Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder
# Northwestern University
# EECS 337
# Professor Lawrence Birnbaum
# 11 February 2015

# This file should probably only include a main function with as little code as possible. We want to abstract our code
# as much as possible by defining functions and classes externally in the modules folder so that we can all be working
# on the project simultaneously with as little conflict as possible.

import sys

import modules.util as util
from modules.parser import parse_tweets

__author__ = "Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder"
__credits__ = ["Kristen Amaddio", "Neal Kfoury", "Michael Nowakowski", "Adam Snyder"]
__status__ = "Development"


def main():
    """
    Executes the Golden Globes program, which analyzes a set of tweets and outputs information about the event that
    they are describing.

    Command line arguments:
    twitter_json -- a JSON formatted database of tweets
    """
    args = sys.argv[1:]
    if not args:
        print util.correct_usage

    # Just some mock skeleton code...
    # None of these functions are defined yet
    load_tweets(args(0))
    parse_tweets()
    sort_tweets()
    build_model()
    print_results()

if __name__ == '__main__':
    main()