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

import threading

import modules.cmd_line as cmd_line
import modules.process_hosts as process_hosts
import modules.process_start_time as process_start_time
from modules.util import vprint
from modules.Result import Result
from modules.Database import Database

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
    # raw_input('Shall we begin execution? ')
    process_tweets(db, result)
    result.print_results()


def process_tweets(db, result):
    """Calls helper (multithreaded) functions to process tweets as they arrive"""

    # To add new processes, just add to the threads dictionary defined here:
    threads = {
        'hosts': threading.Thread(target=process_hosts.run, args=(db, result)),
        'start_time': threading.Thread(target=process_start_time.run, args=(db, result))
    }

    for name, thread in threads.items():
        vprint('Process ' + name + ' started')
        thread.start()
    all_done = False
    while not all_done:
        all_done = True
        for name, thread in threads.items():
            thread.join(0.1)
            if thread.is_alive():
                all_done = False
            else:
                vprint('Process ' + name + ' finished')
                del threads[name]
    return


if __name__ == '__main__':
    main()