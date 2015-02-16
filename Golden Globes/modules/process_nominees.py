# Processes tweets to find the nominees
# Produces ordered list of tuples representing most popular names (as defined by regex.name) appearing in tweets
# matched by regex.subjunctive
# TODO: Match to categories (Zinger)

import operator
import imdb
ia = imdb.IMDb()
import nltk

import regex
import util
import sys


def run(db, target):
    names = {}
    #cursor = db.collection.find({"text": regex.subjunctive})
    cursor = db.collection.find({"text": regex.israel, 'retweeted_status': {'$exists': False}})
    with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch1.txt', 'w') as f:
        for award in target.awards:
            subcursor = cursor.find()
        for tweet in subcursor:
            # f.write(tweet['text'].encode('ascii','ignore')+'\n')
            # continue
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
        # sys.exit()
        r = sorted(names.items(), key=operator.itemgetter(1), reverse=True)
        for i in r:
            f.write(i[0]+'\n')


def weed_out(name, target):
    hits = ia.search_person(name)
    if not hits:
        return True
    if name in target.hosts:
        return True
    if name in target.winning_people:
        return True
    return False


def category_search(name, target):
    return


def success_rate():
    with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\actual_nominees.txt', 'r') as a:
        with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch1.txt', 'w') as q:
            i=0
            aa = a.readlines()
            qq = q.readlines()
            for d in aa:
                if d in qq:
                    i += 1
            print 'success: %s' % i