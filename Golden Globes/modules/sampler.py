#!/Users/flame/anaconda/bin/python

# An executable file with functions that grab samples from tweet data
# This will likely NOT be used as a part of our final program, but it's nice for testing

import os
import sys
import json
import numpy
import unicodedata
import re
import util


def main():
    # Parses command line arguments and runs respective function
    usage = 'usage: [random | verified | generate] json_file [dest] sample_size [detail_level=2] [repetitions]'
    args = sys.argv[1:]
    if len(args) == 0:
        print usage
        sys.exit(1)
    elif 1 <= len(args) <= 2:
        if args[0] == 'random':
            print 'usage: random json_file sample_size'
        elif args[0] == 'verified':
            print 'usage: verified json_file sample_size'
        elif args[0] == 'generate':
            print 'usage: generate source_json dest_dir sample_size [detail_level] [repetitions]'
        else:
            print 'usage: generate source_json dest_dir sample_size [detail_level] [repetitions]'
        sys.exit(1)
    elif len(args) == 3:
        if args[0] == 'random':
            print_random(args[1], int(args[2]))
        elif args[0] == 'verified':
            print_verified(args[1], int(args[2]))
        elif args[0] == 'generate':
            print 'usage: generate source_json dest_dir sample_size [detail_level] [repetitions]'
            sys.exit(1)
        else:
            print 'usage: generate source_json dest_dir sample_size [detail_level] [repetitions]'
            sys.exit(1)
    elif len(args) == 4 and args[0] == 'generate':
        generate_sample(args[1], args[2], args[3])
    elif len(args) == 5 and args[0] == 'generate':
        generate_sample(args[1], args[2], args[3], int(args[4]))
    elif len(args) == 6 and args[0] == 'generate':
        for i in range(int(args[5])):
            generate_sample(args[1], args[2], args[3], int(args[4]))
    else:
        print usage
        sys.exit(1)


def make_random_sample(json_filename, number_of_samples):
    """generates a list of (time, tweet_text) given a json file and sample size"""

    if not os.path.isfile(json_filename):
        sys.exit(1)
    selection = get_random_selection(number_of_samples, 1754153)
    sample = []
    with open(json_filename, 'r') as json_file:
        i = 1
        for line in json_file:
            if not selection:
                break
            if i == selection[0]:
                selection.pop(0)
                tweet = json.loads(line)
                sample.append((tweet['created_at'], tweet['text']))
            i += 1
    return sample


def make_verified_sample(json_filename, number_of_samples):
    """generates a list of (time, tweet_text) from only verified twitter users given a json file and sample size"""

    if not os.path.isfile(json_filename):
        sys.exit(1)
    tweets = []
    with open(json_filename, 'r') as json_file:
        for line in json_file:
            tweet = json.loads(line)
            if tweet['user']['verified']:
                tweets.append((tweet['created_at'], tweet['text'], tweet['user']['screen_name']))
    selection = get_random_selection(number_of_samples, 38111)
    print len(tweets)
    print len(selection)
    sample = []
    i = 1
    for tweet in tweets:
        if not len(selection):
            break
        if i == selection[0]:
            selection.pop(0)
            sample.append(tweet)
        i += 1
    return sample


def print_sample(sample):
    """prints a sample of tweets"""

    number_of_samples = len(sample)
    sample_type = len(sample[0])
    f = open('sample_of_'+str(number_of_samples)+'.txt', 'w')
    i = 0
    if sample_type == 2:
        for time, text in sample:
            u_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
            f_text = re.sub('\s+', ' ', u_text)
            if f_text:
                i += 1
            f.write(time+'   '+f_text+'\n')
    if sample_type == 3:
        for time, text, username in sample:
            u_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
            f_text = re.sub('\s+', ' ', u_text)
            if f_text:
                i += 1
            f.write(time+'  '+username+':  '+f_text+'\n')
    return str(i) + 'lines wrote'


def get_random_selection(num, total_tweets):
    """generates a list of random numbers from 1 to 1754153 given a sample size"""
    selection = []
    while len(selection) < int(num):
        selection.extend(numpy.random.random_integers(1, total_tweets, int(num)-len(selection)))
        selection = list(set(selection))
    return sorted(selection)


def print_verified(json_filename, number_of_samples):
    """prints random verified tweets json file and sample size"""
    return print_sample(make_verified_sample(json_filename, number_of_samples))


def print_random(json_filename, number_of_samples):
    """prints random tweets, given a json file and sample size"""
    return print_sample(make_random_sample(json_filename, number_of_samples))


def generate_sample(source, dest, num, detail=2):
    """generates a JSON sample of a larger corpus of JSON data
    useful for running tests"""
    if detail not in (1, 2, 3):
        detail = 3

    if not os.path.isfile(source):
        util.warning('Not a valid source file')
        sys.exit(1)
    if not os.path.isdir(dest):
        util.warning('Not a valid destination')
        sys.exit(1)
    try:
        source_name_match = re.search(r'(\w+).json', str(source)).group(1)
    except AttributeError:
        util.warning('Not a valid JSON source file')
        sys.exit(1)

    files_nums_in_dest = []
    file_num = 0
    for f in os.listdir(dest):
        if os.path.isfile(os.path.join(dest, f)):
            match = re.search(source_name_match + r'_' + str(detail) + r'_(\d\d)_\d+\.json', f)
            if match:
                files_nums_in_dest.append(int(match.group(1)))
    for i in range(1, 99):
        if i not in files_nums_in_dest:
            file_num = i
            break
    print 'Reading ', source
    num_lines = sum(1 for line in open(source))
    selection = get_random_selection(num, num_lines)
    select_len = len(selection)
    f_o_name = source_name_match + '_' + str(detail) + '_' + str(file_num).zfill(2) + '_' + str(num) + '.json'
    f_o_path = os.path.join(dest, f_o_name)
    print 'Building ', f_o_path
    f_o = open(f_o_path, 'w')
    with open(source, 'r') as f_i:
        i = 1
        for line in f_i:
            if not len(selection):
                break
            if i == selection[0]:
                del selection[0]
                if detail == 1:
                    json_data = build_json(line, 'text', 'created_at')
                elif detail == 2:
                    json_data = build_json(line, 'text', 'created_at', 'user->lang', 'user->favourites_count',
                                           'user->verified', 'user->followers_count')
                else:
                    json_data = json.loads(line)
                json.dump(json_data, f_o)
                if len(selection):
                    f_o.write('\n')
            i += 1
        if len(selection):
            util.warning('file closed early on i='+str(i)+' ('+str(select_len-len(selection))+'/'+str(select_len) +
                         ' processed), next item: '+str(selection[0]))
            sys.exit(1)

    print 'Done!'


def build_json(line, *args):
    data_in = json.loads(line)
    data_out = {}
    for arg in args:
        arg_s = arg.split('->')
        if len(arg_s) == 2:
            try:
                data_out[arg_s[0]]
            except KeyError:
                data_out[arg_s[0]] = {}
            data_out[arg_s[0]][arg_s[1]] = data_in[arg_s[0]][arg_s[1]]
        else:
            data_out[arg] = data_in[arg]
    return data_out


if __name__ == '__main__':
    main()