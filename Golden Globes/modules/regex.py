# System RegExs

import re
import util


# -- General Use -- #

def optional_space(text):
    return text.replace(' ', ' ?')

# TODO: generalize names for all shows
name = re.compile(r'\b(?!Golden|Best)([A-Z]([a-z]+|[.A-Z] ?){1,3} )[A-Z][a-z][A-Z]?[a-z]*')
subjunctive = re.compile(r'\bhop[ei]|\bwish|\bwant|\bshould', re.I)
congrat = re.compile(r'congrats|congratulations', re.I)


# -- Hosts -- #

hosts = re.compile(r'host', re.I)


# -- Starting Time -- #

time = re.compile(optional_space(util.show_name) + r'.*at (\d+):?\d* *([ap]m) ?(\w\w?\w?T)', re.I)


# -- Nominees -- #

nominees = re.compile(r'\bnomi?')


#  -- Winners -- #

winners = re.compile(r'(.*)\b(won|wins)(.*)\bfor\b(.*)')


# -- Obscure -- #

israel = re.compile(r'(?=.*\bEthan Hawke\b)(?=.*\bMark Ruffalo\b).*', re.I)
