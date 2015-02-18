# Processes tweets to find the winners

import datetime
import twitter
import nltk
import math

import regex
from util import vprint
import util
import twitter_app


def run(db, target, event, event2):
    """Determines winners, awards, and creates ceremony time line"""
    event.wait()  # Wait for start_time to be set
    vprint('Received start time. Finding winners...')
    raw_winners = read_winners(db, target)
    vprint('Processing winners...')
    processed_winners = consolidate_winners(raw_winners)
    vprint('Sorting winners...')
    sorted_winners = sorted(processed_winners.items(), key=sort_winners, reverse=True)
    vprint('Getting top winners...')
    top_winners = get_top_winners(sorted_winners)
    consolidated_winners = super_consolidate(top_winners)
    sorted_super = sorted(consolidated_winners.items(), key=sort_winners, reverse=True)
    target.winners = match_to_awards(sorted_super)
    event2.set()


def sort_winners(key):
    return len(key[1])


def consolidate_winners(winner_bins):
    """Takes in raw winner:[awards] data and processes it by
        1. Resolving twitter handles to real names
        2. Resolving hashtags to real names
        3. Removing winners using a stop list"""
    winners = {}
    for winner_name, awards in winner_bins.items():
        if winner_name:
            if winner_name[0] == '@':
                if util.search_twitter_handles:
                    winner_name = handle_lookup(winner_name)
                else:
                    continue
            elif winner_name[0] == '#':
                winner_name = split_hashtag(winner_name)
            winner_name = winner_name.lower()
            winner_tokens = nltk.word_tokenize(winner_name)
            winner_passes = False
            for token in winner_tokens:
                if token not in util.common_words:
                    winner_passes = True
                    break
            if not winner_passes:
                continue
            if winner_name in winners.keys():
                winners[winner_name].extend(awards)
            else:
                winners[winner_name] = awards
    return winners


def get_top_winners(winner_bins):
    """Given a dictionary of winners, strips away any that are not mentioned under a set threshold"""
    total = 0
    so_far = 0
    result = []
    for winner, value in winner_bins:
        total += len(value)
    thresh = total * util.winner_threshold
    for winner, value in winner_bins:
        if so_far > thresh:
            break
        result.append((winner, value))
        so_far += len(value)
    return result


def super_consolidate(winner_bins):
    """Takes a dictionary of top winners and attempts to merge similar winner names"""
    result = {}
    # ref_dict = {name: None for name, value in winner_bins}
    ref_dict = {}
    for i in range(len(winner_bins)):
        for j in range(len(winner_bins)):
            if i == j:
                continue
            if winner_bins[i][0] in winner_bins[j][0]:
                if winner_bins[i][0] in ref_dict:
                    ref_dict[winner_bins[j][0]] = ref_dict[winner_bins[i][0]]
                elif winner_bins[j][0] in ref_dict:
                    ref_dict[winner_bins[i][0]] = ref_dict[winner_bins[j][0]]
                elif i > j:
                    ref_dict[winner_bins[j][0]] = winner_bins[j][0]
                    ref_dict[winner_bins[i][0]] = winner_bins[j][0]
                else:
                    ref_dict[winner_bins[j][0]] = winner_bins[i][0]
                    ref_dict[winner_bins[i][0]] = winner_bins[i][0]
    for name, value in winner_bins:
        if name in ref_dict:
            simplified_name = ref_dict[name]
        else:
            simplified_name = name
        if simplified_name in result:
            result[simplified_name].extend(value)
        else:
            result[simplified_name] = value
    return result


def handle_lookup(winner_name):
    """Translates a handle into a name"""
    result = winner_name
    match = regex.twitter_handel.search(winner_name)
    if match:
        try:
            result = twitter_app.twitter_api.users.show(screen_name=match.group(1))['name']
        except twitter.api.TwitterHTTPError:
            pass
    return result


def split_hashtag(hashtag):
    """Translates a hashtag into a space-delimited string"""
    result = ''
    for letter in hashtag:
        if letter == '#':
            continue
        if letter.islower():
            result += letter
        elif result:
            result += ' ' + letter
        else:
            result += letter
    return result


def read_winners(db, target):
    """Searches a database for winners, matches against some schema, and returns bins award titles with
    winner names as keys"""
    t = target.start_time
    if target.timestamp_format == 'str':
        t = str(t)
    cursor = db.collection.find({"text": regex.winners, 'retweeted_status': {'$exists': False},
                                 'timestamp_ms': {'$gt': t}})
    winner_bins = {}
    for tweet in cursor:
        tweet_time = int(tweet['timestamp_ms'])
        if regex.subjunctive.search(tweet['text']):
            continue
        parsed_tweet = None
        model_num = 0
        for winner_model in regex.winner_models:
            match = winner_model.search(tweet['text'])
            if match:
                parsed_tweet = match
                break
            model_num += 1
        if not parsed_tweet:
            continue
        winner = parsed_tweet.group(1)
        award = parsed_tweet.group(2)
        if winner in winner_bins.keys():
            winner_bins[winner].append((award, tweet_time))
        else:
            winner_bins[winner] = [(award, tweet_time)]
    return winner_bins


def match_to_awards(winners):
    """Takes a winner:[awards] dictionary and returns a list of (winner, award_title, time) tuples"""
    result = []
    for winner, value in winners:
        award_list = []
        time_list = []
        for award, time in value:
            award_list.append(award)
            time_list.append(time)
        award_result = max(set(award_list), key=award_list.count)  # select_best(award_list)
        time_list = sorted(time_list)
        time_result = time_list[int(math.floor(len(time_list)*util.award_time_percentile))]
        result.append((winner, award_result, time_result))
    return sorted(result, key=sort_by_time)


def select_best(award_list):
    buffy = {}
    for award in award_list:
        toks = nltk.word_tokenize(award)
        for tok in toks:
            if tok in buffy:
                buffy[tok] += 1
            else:
                buffy[tok] = 1
    # buffy = {}
    # for award in award_list:
    #     if award in buffer:
    #         buffy[award] += 1
    #     else:
    #         buffy[award] = 1
    # sorted_list = sorted(buffy, key=itemgetter(1), reverse=True)
    # top_list = sorted_list[:math.floor(len(sorted_list)*util.award_name_threshold)]
    # return max(set(top_list), key=award_list.count)


def time_to_seconds(time):
    return (time.replace(tzinfo=None)-datetime.datetime.utcfromtimestamp(0)).total_seconds()


def sort_by_time(winner):
    return winner[2]
