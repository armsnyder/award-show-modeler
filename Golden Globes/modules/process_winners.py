# Processes tweets to find the winners
# TODO: Make regex for winners match more tweets. Make more robust.
    # TODO: Suggest looking at all tweets matching r'w[io]n' and finding a better pattern
# TODO: Apply more NLP to tweet to more accurately figure out...
    # TODO: "Chunks" of the tweet, with chunk A being the part of the tweet containing the winner's name,
        # TODO: chunk B being the award name, and chunk C being what film the winner won for...
    # TODO: Search within each chunk to find the pertinent information
# TODO: Write a function that takes our bins and collapses them by looking up twitter handles, hashtags, etc
# TODO: Write a function that tales the collapsed bins and uses statistical analysis to find the real winners
    # TODO: (possibly using hamming distance)


import nltk
import datetime
from dateutil import tz

import regex
from util import vprint


def run(db, target, event):
    event.wait()  # Wait for start_time to be set
    vprint('Received start time. Processing winners...')
    cursor = db.collection.find({"text": regex.winners})
    for tweet in cursor:
        tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')\
            .replace(tzinfo=tz.gettz('UTC'))
        if weed_out(tweet, target, tweet_time):
            continue
        match = regex.winners.search(tweet['text'])
        winner = get_winner(match)
        award = get_award(match)
        win_for = get_win_for(match)
        if winner in target.winner_bins.keys():
            target.winner_bins[winner]['award'].append((award, tweet_time))
            target.winner_bins[winner]['win_for'].append(win_for)
        else:
            target.winner_bins[winner] = {
                'award': [(award, tweet_time)],
                'win_for': [win_for]
            }
    # display_result(target.winner_bins)


def weed_out(tweet, target, tweet_time):
    # Check for subjunctive
    if regex.subjunctive.search(tweet['text']):
        return True
    # Check if tweet occurs before event starts
    if tweet_time < target.start_time:
        return True
    return False


def is_name(word):
    return word[0].isupper()


def get_winner(match):
    tokens = nltk.word_tokenize(match.group(1))
    result = ''
    found_start = False
    continue_words = ['and']
    for i in range(1, len(tokens)-1):
        token = tokens[-i]
        prev_token = tokens[-i-1]
        if is_name(token) or token in continue_words:
            found_start = True
            result = '%s %s' % (token, result)
        elif token == '@' or token == '#':
            found_start = True
            result = '%s%s' % (token, result)
            break
        elif prev_token == '@' or prev_token == '#':
            found_start = True
            result = '%s%s %s' % (prev_token, token, result)
            break
        elif found_start:
            break
    return result[:-1]


def get_winner_as_list(match):
    tokens = nltk.word_tokenize(match.group(1))
    result = []
    found_start = False
    continue_words = ['and']
    for i in range(1, len(tokens)-1):
        token = tokens[-i]
        prev_token = tokens[-i-1]
        if is_name(token) or token in continue_words:
            found_start = True
            result.append(token)
        elif token == '@' or token == '#':
            found_start = True
            result.append(token)
            break
        elif prev_token == '@' or prev_token == '#':
            found_start = True
            result.append(token)
            result.append(prev_token)
            break
        elif found_start:
            break
    return reversed(result)


def get_award(match):
    return nltk.word_tokenize(match.group(3))


def get_win_for(match):
    tokens = nltk.word_tokenize(match.group(4))
    result = []
    stop_list = ['.', '!', '?']
    for token in tokens:
        if token in stop_list:
            break
        else:
            result.append(token)
    return result


def display_result(bins):
    """Just for debugging"""
    with open('/Users/flame/Desktop/output.txt', 'w') as f:
        f.seek(0)
        f.truncate()
        for winner, value in bins.items():
            if winner:
                f.write(winner.encode('utf8')+':\r\n')
            f.write('\tAwards:\r\n')
            for award, time in value['award']:
                f.write('\t\t')
                for award_e in award:
                    f.write('('+award_e.encode('utf8')+') ')
                f.write('\r\n')
            f.write('\tWins For:\r\n')
            for win_for in value['win_for']:
                f.write('\t\t')
                for win_for_e in win_for:
                    f.write('('+win_for_e.encode('utf8')+') ')
                f.write('\r\n')