# System RegExs

import re
import util
import datetime


# -- General Use -- #

def optional_space(text):
    return text.replace(' ', ' ?')

name = re.compile(r'\b(?!Best)(?:[A-Z](?:[a-z]+|[.A-Z] ?){1,3} )[A-Z][a-z][A-Z]?[a-z]*')
subjunctive = re.compile(r'\bhop[ei]|\bwish|\bwant|\bshould|\bthink', re.I)
congrat = re.compile(r'congrats|congratulations', re.I)
hashtag = re.compile(r'#((?:[A-Z][a-z]+)+)')


def update_name_regex(event_name):
    global name, time
    parsed_event = event_name.replace(' ', '|')
    name = re.compile(r'\b(?!'+parsed_event+'|Best)(?:[A-Z](?:[a-z]+|[.A-Z] ?){1,3} )[A-Z][a-z][A-Z]?[a-z]*')
    time = re.compile(optional_space(event_name) + r'.*at (\d+):?\d* *([ap]m) ?(\w\w?\w?T)', re.I)


# -- Hosts -- #

hosts = re.compile(r'host', re.I)


# -- Starting Time -- #

time = re.compile(r'.*at (\d+):?\d* *([ap]m) ?(\w{1,3}T)', re.I)


# -- Nominees -- #

nominees = re.compile(r'\bnomi?')
eehhhh = re.compile(r'(.*) should(?:(?:\'ve)|(?: have))(?: (?:been|won|got(?:ten)?) (.*)\W?)?', re.I)
eh = re.compile(r'(if (.*) wins)', re.I)


#  -- Winners -- #

winners = re.compile(r'(?=.*best)\bw[io]n', re.I)
best_str = r'(\bbest.+?)(?:!|\.|\?|\bon\b|\bfrom|\bfor|\bat|http)'
winner_models = [
    re.compile(r'([@#]\w+) w[io]n.*' + best_str, re.I),
    re.compile(r'\bcongrat.*? (?:to )?(.*?) (?:\bon\b|\bfrom|\bfor).*' + best_str, re.I),
    re.compile(r'[\.\?!:] (.*) w[io]n.*' + best_str, re.I)
    ]
if util.search_twitter_handles:
    winner_models.append(re.compile(r'[#@]\w* (.*) w[io]n.*' + best_str, re.I))
winner_models.append(re.compile(r'(.*) w[io]n.*' + best_str, re.I))

twitter_handel = re.compile(r'(@\w+)')


# -- Time Manipulation --#

def time_model(hour, minute, offset):
    s = r'%02d:%02d:' % (hour, minute + offset)
    return re.compile(s)


# def get_hour_minute(time_string):
#     result = []
#     t = re.match(r'([0-9]{2}):([0-9]{2}):([0-9]{2})', time_string)
#     result[0] = t.group(1)
#     result[1] = t.group(2)
#     result[2] = t.group(3)
#     return result
#
#
# def generate_time_models(hour, minute, second, range, direction):
#     result = []
#     if direction == "pre":
#         for i in range:
#             if int(minute) - (direction * i) < 0:
#
#             str = r'%s:%s:[0-9]{2}' % hour, minute - (direction * i),
#             result.append(re.compile(str))
#     return result



# -- Result -- #

output = re.compile(r'output_(\d+)\.json')


# -- Obscure -- #

israel = re.compile(r'.*Ethan Hawke.*', re.I)

# -- Red Carpet -- #
best_dressed = re.compile(r'#(\w*best+\w*dress)', re.I)
worst_dressed = re.compile(r'#(\w*wors+\w*dress)', re.I)
outfit = re.compile(r'wear|wore', re.I)


# -- Time Functions -- #

# def delta_time(date, start, end):
#     """Given a datetime and a start and end (measured in delta seconds), compute a regex"""
#     start_time = date + datetime.timedelta(0, int(start))
#     end_time = date + datetime.timedelta(0, int(end))
#     return re.compile(dt_helper(start_time, end_time))
#
#
# def dt_helper(start, end, phase='day', cutoff=0):
#     if phase == 'day':
#         start_str = '%02d' % start.day
#         end_str = '%02d' % end.day
#         if start.day == end.day:
#             return start_str + ' ' + dt_helper(start, end, 'hour')
#         else:
#             return \
#                 start_str + ' ' + dt_helper(start, end, 'hour', -1) + '|' + \
#                 end_str + ' ' + dt_helper(start, end, 'hour', 1)
#     elif phase == 'hour':
#         start_str = '%02d' % start.hour
#         end_str = '%02d' % end.hour
#         if cutoff > 0:
#             return dt_helper(datetime.datetime(start.year, start.month, start.day, 0, 0, 0), end, 'hour')
#         elif cutoff < 0:
#             return dt_helper(start, datetime.datetime(start.year, start.month, start.day, 23, 59, 59), 'hour')
#         else:
#             if start.hour == end.hour:
#                 return '(?:' + start_str + ':' + dt_helper(start, end, 'min') + ')'
#             else:
#                 return '(?:' + \
#                 start_str + ':' + dt_helper(start, end, 'min', -1) + '|' + \
#                 end_str + ':' + dt_helper(start, end, 'min', 1) + ')'
#     elif phase == 'min':
#         start_str = '%02d' % start.minute
#         end_str = '%02d' % end.minute
#         if cutoff > 0:
#             return dt_helper(datetime.datetime(start.year, start.month, start.day, start.hour, 0, 0), end, 'min')
#         elif cutoff < 0:
#             return dt_helper(start, datetime.datetime(start.year, start.month, start.day, start.hour, 59, 59), 'min')
#         else:
#             if start.minute == end.minute:
#                 return '(?:' + start_str + ')'
#             else:
#                 minute_diff = end.minute - start.minute
#                 if minute_diff == 1:
#                     return '(?:' + start_str + '|' + end_str + ')'
#                 else:
#                     result = '(?:' + start_str + '|'
#                     for i in range(start.minute+1, end.minute):
#                         result += '%02d' % i + '|'
#                     result += end_str + ')'
#                     return result
