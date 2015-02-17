import re
from Database import Database
from Result import Result
import datetime

# print '%02d' % dd
#
# time_pat = re.compile(r'')
# db = Database('gg', 'tweets.json', False)
# result = Result()
#
# cursor = db.collection.find({'created_at': re.compile(r'05:((51:5[5-9])|(52:((0\d)|1[0-5])))')})
# for tweet in cursor:
#     print tweet['created_at']


def delta_time(date, start, end):
    """Given a datetime and a start and end (measured in delta seconds), compute a regex"""
    start_time = date + datetime.timedelta(0, int(start))
    end_time = date + datetime.timedelta(0, int(end))
    return re.compile(dt_helper(start_time, end_time))


def dt_helper(start, end, phase='day', cutoff=0):
    if phase == 'day':
        start_str = '%02d' % start.day
        end_str = '%02d' % end.day
        if start.day == end.day:
            return start_str + ' ' + dt_helper(start, end, 'hour')
        else:
            return \
                start_str + ' ' + dt_helper(start, end, 'hour', -1) + '|' + \
                end_str + ' ' + dt_helper(start, end, 'hour', 1)
    elif phase == 'hour':
        start_str = '%02d' % start.hour
        end_str = '%02d' % end.hour
        if cutoff > 0:
            return dt_helper(datetime.datetime(start.year, start.month, start.day, 0, 0, 0), end, 'hour')
        elif cutoff < 0:
            return dt_helper(start, datetime.datetime(start.year, start.month, start.day, 23, 59, 59), 'hour')
        else:
            if start.hour == end.hour:
                return '(' + start_str + ':' + dt_helper(start, end, 'min') + ')'
            else:
                return '(' + \
                start_str + ':' + dt_helper(start, end, 'min', -1) + '|' + \
                end_str + ':' + dt_helper(start, end, 'min', 1) + ')'
    elif phase == 'min':
        start_str = '%02d' % start.minute
        end_str = '%02d' % end.minute
        if cutoff > 0:
            return dt_helper(datetime.datetime(start.year, start.month, start.day, start.hour, 0, 0), end, 'min')
        elif cutoff < 0:
            return dt_helper(start, datetime.datetime(start.year, start.month, start.day, start.hour, 59, 59), 'min')
        else:
            if start.minute == end.minute:
                return '(' + start_str + ')'
            else:
                minute_diff = end.minute - start.minute
                if minute_diff == 1:
                    return '(' + start_str + '|' + end_str + ')'
                else:
                    result = '(' + start_str + '|'
                    for i in range(start.minute+1, end.minute):
                        result += '%02d' % i + '|'
                    result += end_str + ')'
                    return result

dd = datetime.datetime(2015, 1, 12, 7, 55, 16)
print delta_time(dd, -2000, 2000).pattern

# assert construct_delta_time_regex(datetime.datetime(2015, 1, 2, 5, 30, 30), 0, 10) == \
#     r'02 05:30:[3-4]\d'
