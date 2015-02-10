# System RegExs

import re
import util


# -- General Use -- #

def optional_space(text):
    return text.replace(' ', ' ?')


subjunctive = re.compile(r'\bhope|\bwish|\bwant', re.I)
congrat = re.compile(r'congrats|congratulations', re.I)

# -- Starting Time -- #

time = re.compile(optional_space(util.show_name) + r'.*at (\d+):?\d* *([ap]m) ?(\w\w?\w?T)', re.I)


# -- Nominees -- #

nominees = re.compile(r'\bnomi?')


#  -- Winners -- #

winners = re.compile(r'\b(won|wins)(.*)\bfor\b(.*)')


# -- Obscure -- #

israel = re.compile(r'(?=.*\bEthan Hawke\b)(?=.*\bMark Ruffalo\b).*', re.I)
