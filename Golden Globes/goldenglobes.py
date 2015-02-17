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
import os

import modules.cmd_line as cmd_line
import modules.process_hosts as process_hosts
import modules.process_start_time as process_start_time
import modules.process_winners as process_winners
import modules.process_presenters_and_noms as process_presenters_and_noms
import modules.process_best_dressed as process_best_dressed
import modules.process_worst_dressed as process_worst_dressed
from modules.Result import Result
from modules.Database import Database
from modules.util import vprint
import autograder.autograder as autograder
import modules.util as util
import modules.GUI

__author__ = "Kristen Amaddio, Neal Kfoury, Michael Nowakowski, and Adam Snyder"
__credits__ = ["Kristen Amaddio", "Neal Kfoury", "Michael Nowakowski", "Adam Snyder"]
__status__ = "Development"


def main():
    """
    Executes the Golden Globes program, which analyzes a set of tweets and outputs information about the event that
    they are describing.
    """
    util.script_path = os.path.dirname(os.path.realpath(__file__))
    db = Database(cmd_line.args.database, cmd_line.args.collection, cmd_line.args.force_reload)
    result = Result()
    # raw_input('Shall we begin execution? ')
    process_tweets(db, result)
    db.conn.close()
    result.print_results()
    output = result.print_output_file()
    if cmd_line.args.run_autograder:
        autograder.main(output)
    modules.GUI.html_done()


def process_tweets(db, result):
    """Calls helper (multithreaded) functions to process tweets as they arrive"""

    # Define events that allow threads to communicate and wait for one another:
    event_names = ['start_time_set', 'winners_found']

    events = {}
    for event_name in event_names:
        events[event_name] = threading.Event()

    # To add new processes, start new threads like so:
    threading.Thread(name='Process Hosts',
                     target=process_hosts.run,
                     args=(db, result)).start()
    threading.Thread(name='Best Dressed',
                     target=process_best_dressed.run,
                     args=(db, result)).start()
    threading.Thread(name='Worst Dressed',
                     target=process_worst_dressed.run,
                     args=(db, result)).start()
    threading.Thread(name='Process Start Time',
                     target=process_start_time.run,
                     args=(db, result, events['start_time_set'])).start()
    threading.Thread(name='Process Winners',
                     target=process_winners.run,
                     args=(db, result, events['start_time_set'], events['winners_found'])).start()
    threading.Thread(name='Process Presenters and Nominees',
                     target=process_presenters_and_noms.run,
                     args=(db, result, events['winners_found'])).start()

    main_thread = threading.currentThread()
    for thread in threading.enumerate():
        if thread is main_thread:
            continue
        vprint('%s starting' % thread.name)
    for thread in threading.enumerate():
        if thread is main_thread:
            continue
        thread.join()
        vprint('%s finished' % thread.name)

    return


if __name__ == '__main__':
    util.script_path = os.path.dirname(os.path.realpath(__file__))
    main()