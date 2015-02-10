# nom nom nom

import nltk
import regex


def run(db, target):
    cursor = db.collection.find({'text': regex.nominees})
    with open('C:\\Users\\Neal\\Documents\\Coursework\\EECS\\337\\scratch2.txt', 'w') as noms:
        for tweet in cursor:
            t = nltk.word_tokenize(tweet['text'])

            t_pr = ''
            for b in t:
                t_pr += '(' + b + ') '
            # p_tweet = nltk.word_tokenize(tweet['text'])
            noms.write(tweet['user']['screen_name']+' ')
            noms.write(tweet['text'].encode('utf8')+'\n')
