# Code for interfacing with command line arguments passed to our program
# Don't worry about understanding this.

import argparse
import util

parser = argparse.ArgumentParser(description='Discover information about an awards ceremony by processing tweets')
group = parser.add_mutually_exclusive_group()

parser.add_argument('-v', '--verbose', action='store_true',
                    help='Show additional system messages')

parser.add_argument('-d', '--database', default=util.default_database,
                    help='Mongo database where tweets live')

group.add_argument('-c', '--collection', default=util.default_collection,
                   help='Specify which Mongo collection to load')

group.add_argument('-t', '--twitter_json', dest='collection', metavar='TWITTER_JSON',
                   help='JSON file holding tweet objects. If specified, will attempt to load the JSON objects therein '
                        'into a collection by the same name.')

parser.add_argument('-f', '--force_reload', action='store_true',
                    help='Force reloading tweets JSON into mongoDB')

group.add_argument('-e', '--event_name', default=util.event_name, dest=util.event_name,
                   help='Specify name of the award show to process')

args = parser.parse_args()

if args.verbose:
    util.verbose = True