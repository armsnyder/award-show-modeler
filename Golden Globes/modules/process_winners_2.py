# Processes tweets to find the winners

import re
import nltk

award_words = ('Motion', 'Picture', 'Drama', 'Actress', 'Actor', 'Musical', 'Comedy', 'Animates', 'Feature', 'Film',
               'Foreign', 'Language', 'Supporting', 'Director', 'Screenplay', 'Original', 'Score', 'Song', 'TV',
               'Television', 'Series', 'Movie', 'Mini-Series')
award_stop = ('in', 'In', 'a', 'A', 'or', 'Or', ',', '-', '--', ':')


def run(db, target):
    pattern = re.compile(r'Best')
    cursor = db.collection.find({"text": pattern})
    result = []
    award_frequency = get_award_frequency(db)
    for tweet in cursor:
        tokens = nltk.word_tokenize(tweet['text'])
        award_name = []
        for i in range(len(tokens)):
            if tokens[i] == 'Best':
                i += 1
                for j in range(len(tokens[i:])):
                    if tokens[i+j] in award_stop:
                        continue
                    elif tokens[i+j] in award_words:
                        award_name.append(tokens[i+j])
                    else:
                        break
                break
        if not len(award_name):
            continue
        assign_bin(award_name, target, award_frequency)


def get_award_frequency(db):
    award_freq = {}
    for award in award_words:
        award_freq[award] = 0
    pattern = re.compile(r'Best')
    cursor = db.collection.find({"text": pattern})
    for tweet in cursor:
        tokens = nltk.word_tokenize(tweet['text'])
        for i in range(len(tokens)):
            if tokens[i] == 'Best':
                i += 1
                for j in range(len(tokens[i:])):
                    if tokens[i+j] in award_stop:
                        continue
                    elif tokens[i+j] in award_words:
                        award_freq[tokens[i+j]] += 1
                    else:
                        break
                break
    award_freq_tuple = []
    for key, value in award_freq.items():
        award_freq_tuple.append((key, value))
    return award_freq_tuple


def assign_bin(award_name, target, freq_list):
    return