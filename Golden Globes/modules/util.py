# Contains non-specific utility functions and strings

import sys

# -- STRINGS --#

correct_usage = "usage: twitter_json"


# -- METHODS -- #

def warning(text):
    """prints a custom error message to console"""
    sys.stderr.write("WARNING: "+text+"\n")


def close(var):
    """for debugging, exists program and outputs some variable"""
    print var
    sys.exit(0)