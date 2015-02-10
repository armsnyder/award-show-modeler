# Processes tweets to find the nominees
# Produces ordered list of tuples representing most popular names (as defined by regex.name) appearing in tweets
# matched by regex.subjunctive
# TODO: Match to categories (Zinger)

import operator

import regex


def run(db, target):
    names = {}
    cursor = db.collection.find({"text": regex.subjunctive})
# with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch1.txt', 'w') as f:
    for tweet in cursor:
        n = regex.name.match(tweet['text'])
        if n:
            if n.group() in names:
                names[n.group()] += 1
            elif not weed_out(n.group(), target):
                names[n.group()] = 1
        else:
            continue
    print sorted(names.items(), key=operator.itemgetter(1), reverse=True)


def weed_out(name, target):
    if name in target.hosts:
        return True
    if name in target.winning_people:
        return True
    return False