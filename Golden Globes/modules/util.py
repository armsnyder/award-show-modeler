# Contains non-specific utility functions and strings

import sys
from nltk.corpus import stopwords
import operator

# -- FIELDS -- #

verbose = True  # if True, will FORCE print out of additional debug messages using vprint
default_collection = 'samples/goldenglobes2015_2_05_386000.json'  # default tweet JSON
default_database = 'gg'  # default MongoDB database (Miriam's is gg)
host_threshold = 0.9
show_name = 'Golden Globes'
common_words = set(stopwords.words('english'))

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
