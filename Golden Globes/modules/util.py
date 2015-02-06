# Contains non-specific utility functions and strings

import sys

# -- FIELDS -- #

verbose = True  # if True, will FORCE print out of additional debug messages using vprint
default_collection = 'samples/goldenglobes2015_2_05_386000.json'  # default tweet JSON
default_database = 'gg'  # default MongoDB database (Miriam's is gg)


# -- METHODS -- #

def warning(text, exit=False, status=1):
    """prints a custom error message to console"""
    if exit:
        sys.stderr.write("FATAL ERROR: "+text+"\n")
        sys.exit(status)
    else:
        sys.stderr.write("WARNING: "+text+"\n")
    return


def close(var):
    """for debugging, exits program and outputs some variable"""
    print var
    sys.exit(0)


def vprint(text):
    """prints a custom message to console if in verbose mode"""
    if verbose:
        print text
    return