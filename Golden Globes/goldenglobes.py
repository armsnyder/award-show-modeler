#!/Users/flame/anaconda/bin/python
# Golden Globes Natural Language Processor
# by Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder
# Northwestern University
# EECS 337
# Professor Lawrence Birnbaum
# 11 February 2015

# This file should probably only include a main function with as little code as possible. We want to abstract our code
# as much as possible by defining functions and classes externally in the modules folder so that we can all be working
# on the project simultaneously with as little conflict as possible.

import modules.cmd_line as cmd_line
from modules.Database import Database
import re
import threading
import modules.process_hosts as process_hosts
from modules.Result import Result

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

    db = Database(cmd_line.args.database, cmd_line.args.collection, cmd_line.args.force_reload)
    result = Result()
    raw_input('Shall we begin execution? ')
    process_tweets(db, result)
    result.print_results()


def process_tweets(db, result):
    """loads tweets into memory and calls helper (multithreaded) functions to process tweets as they arrive"""
    thread_hosts = threading.Thread(target=process_hosts.process_hosts, args=(db, result))
    thread_hosts.start()
    while thread_hosts.is_alive():
        thread_hosts.join(1)
        print "Analyzing..."
    return


if __name__ == '__main__':
    main()