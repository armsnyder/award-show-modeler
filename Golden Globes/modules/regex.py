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
eehhhh = re.compile(r'(.*) should(?:(?:\'ve)|(?: have))(?: been (.*)\W?)?', re.I)
eh = re.compile(r'(if (.*) wins)', re.I)

#  -- Winners -- #

winners = re.compile(r'(?=.*best)\bw[io]n', re.I)
best_str = r'([# ]best.+?)(?:!|\.|\?|\bon\b|\bfrom|\bfor|\bat)'
winner_models = [
    re.compile(r'([@#]\w+) w[io]n.*' + best_str, re.I),
    re.compile(r'\bcongrat.*? (?:to )?(.*?) (?:\bon\b|\bfrom|\bfor).*' + best_str, re.I),
    re.compile(r'[\.\?!:] (.*) w[io]n.*' + best_str, re.I),
    re.compile(r'[#@]\w* (.*) w[io]n.*' + best_str, re.I),
    re.compile(r'(.*) w[io]n.*' + best_str, re.I)
    ]
twitter_handel = re.compile(r'(@\w+)')

# -- Obscure -- #

israel = re.compile(r'.*Ethan Hawke.*', re.I)
