# Contains non-specific utility functions and strings

import sys

# -- FIELDS -- #

correct_usage = "usage: twitter_json"
verbose = True

# -- METHODS -- #

def warning(text):
    """prints a custom error message to console"""
    sys.stderr.write("WARNING: "+text+"\n")
    return


def close(var):
    """for debugging, exists program and outputs some variable"""
    print var
    sys.exit(0)
    return


def vprint(text):
    """prints a custom message to console if in verbose mode"""
    sys.stderr.write("WARNING: "+text+"\n")
    return