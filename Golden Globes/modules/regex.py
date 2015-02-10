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


# -- Winners -- #

winners = re.compile(r'\bwins(.*)\bfor\b(.*)')


