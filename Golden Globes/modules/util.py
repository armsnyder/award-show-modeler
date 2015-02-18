# Contains non-specific utility functions and strings

import sys
import nltk
import os
import re
import datetime
from dateutil.tz import *

# -- FIELDS -- #

verbose = True  # if True, will FORCE print out of additional debug messages using vprint
search_twitter_handles = False
default_collection = '/Volumes/Navi/Users/flame2/Documents/Northwestern/Y3Q2/EECS 337/gg15mini.json'
# default JSON input or collection name
default_database = 'gg'  # default MongoDB database (Miriam's is gg)
default_output = '$r/output'  # default output JSON destination
output_path = None
script_path = None
host_threshold = 0.85
winner_threshold = 0.545
award_name_threshold = 0.25
award_time_percentile = 0.1
limit = 500  # Imposes limit on some tweet search processes
common_words = list(nltk.corpus.stopwords.words('english'))


def update_common_words(event_name):
    global common_words
    event_name_list = nltk.word_tokenize(event_name.lower())
    for token in event_name_list:
        if token[-1] == 's':
            event_name_list.append(token[:-1])
    common_words.extend(event_name_list)


# -- GENERAL USE METHODS -- #

def warning(text, exit=False, status=1):
    """prints a custom error message to console"""
    if exit:
        sys.stderr.write("FATAL ERROR: "+text+"\n")
        sys.exit(status)
    else:
        sys.stderr.write("WARNING: "+text+"\n")
    return


def close(message=None):
    """for debugging, exits program and outputs some variable"""
    if message:
        print message
    sys.exit(0)


def vprint(text):
    """prints a custom message to console if in verbose mode"""
    if verbose:
        print text
    return


def get_path(path):
    """takes a path and joins it with the path of the calling script"""
    match = re.search(r'\$r/(.*)', path)
    if match:
        result = os.path.join(script_path, match.group(1))
    else:
        result = path
    return result


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1e3, tz=gettz('UTC'))


def timestamp_to_string(timestamp, format_str):
    date = timestamp_to_datetime(timestamp).astimezone(tzlocal())
    return date.strftime(format_str)


def camel_to_space(hashtag):
    """converts camelCase to spaced words"""
    return re.sub(r'([a-z])([A-Z])', r'\g<1> \g<2>', hashtag)