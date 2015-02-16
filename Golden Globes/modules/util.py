# Contains non-specific utility functions and strings

import sys
import nltk
import operator
import twitter
import os
import re

# -- FIELDS -- #

verbose = True  # if True, will FORCE print out of additional debug messages using vprint
search_twitter_handles = False
default_collection = '$r/samples/goldenglobes2015_2_06_386000.json'  # default JSON input or collection name
default_database = 'gg'  # default MongoDB database (Miriam's is gg)
default_output = '$r/output'  # default output JSON destination
output_path = None
script_path = None
host_threshold = 0.8
winner_threshold = 0.545
award_time_percentile = 0.1
event_name = 'Golden Globes'
twitter_key = 'DYcq5c6vadVEe4l8Xnd5Dhu29'
twitter_secret = 'PB0mYw89QYCu9YC63s3bbAxfJr2h07DmJ9zwNlKX4sT1yVbBDR'
twitter_access_token = '80998836-wYMg9lHff0WgBys71LV1SVFwyaaL0XVU17M7Gfx2x'
twitter_access_secret = 'd8MV8XAPJoNs40Z4164uUgMjUwmaqOYRygKm82U9zgD0o'
twitter_api = twitter.Twitter(
    auth=twitter.oauth.OAuth(twitter_access_token, twitter_access_secret, twitter_key, twitter_secret))
common_words = list(nltk.corpus.stopwords.words('english'))
event_name_list = nltk.word_tokenize(event_name.lower())
for token in event_name_list:
    if token[-1] == 's':
        event_name_list.append(token[:-1])
common_words.extend(event_name_list)


# -- METHODS -- #

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


# def select_best(list):
#     result = []
#     disagreement = True
#     i = 0
#     while disagreement:
#         frequencies = {}
#         for item in list:
#             ith_word = item[i]
#             if not ith_word:
#                 list.remove(item)
#                 continue
#             if ith_word in frequencies:
#                 frequencies[ith_word] += 1
#             else:
#                 frequencies[ith_word] = 1
#         if len(frequencies) == 1:
#             disagreement = False
#         r = (sorted(frequencies.items(), key=operator.itemgetter(1), reverse=True))
#         result.append(r[0][0])
#         i += 1
