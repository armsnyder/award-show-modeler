import nltk
import operator

import regex
import util


def run(db, target):
    result = []
    names = {}
    for award, value in target.awards:
        time = value.time()
        cursor = db.collection.find({'created_at': time})
        for tweet in cursor:
            n = regex.name.match(tweet['text'])
            if n:
                n = n.group()
                toks = nltk.word_tokenize(n)
                if toks[0].lower() in util.common_words or toks[1].lower() in util.common_words:
                    continue
                else:
                    if n in names:
                        names[n] += 1
                    # elif not weed_out(n, target):
                    else:
                        names[n] = 1
            else:
                continue
        r = sorted(names.items(), key=operator.itemgetter(1), reverse=True)
        result.append((award, r[0], r[1]))
        target.presenters[award] = (r[0], r[1])


# TODO: figure out how to match a range of timestamps
# TODO: decide how to record result to target


def weed_out(name, target):
    # hits = ia.search_person(name)
    # if not hits:
    #     return True
    if name in target.hosts:
        return True
    if name in target.winning_people:
        return True
    return False