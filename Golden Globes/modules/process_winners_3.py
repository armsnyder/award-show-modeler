# Processes tweets to find the winners

import re
import nltk

award_stop = ('in', 'In', 'a', 'A', 'or', 'Or', ',', '-', '--', ':')


def run(db, target):
    pattern = re.compile(r'Best')
    cursor = db.collection.find({"text": pattern})
    result = []
    for tweet in cursor:
        tokens = nltk.word_tokenize(tweet['text'])
        award_name = []
        for i in range(len(tokens)):
            if tokens[i] == 'Best':
                for j in range(len(tokens[i:])):
                    if tokens[i+j] in award_stop:
                        continue
                    elif is_capital(tokens[i+j]):
                        award_name.append(tokens[i+j])
                    else:
                        break
                break
        if len(award_name) < 2:
            continue
        award_winner = []
        for i in range(len(tokens)):
            if is_capital(tokens[i]) and tokens[i] not in award_stop and tokens[i] not in award_name:
                award_winner.append(tokens[i])
        print ' '.join(award_name), ':', ' '.join(award_winner)


def is_capital(word):
    return word[0].isupper() and word[1:].islower()