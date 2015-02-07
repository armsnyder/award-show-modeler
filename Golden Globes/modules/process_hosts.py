import nltk
import util


def process_hosts(db, target):
    result = {}
    useful_tweets = db.find('host')
    for tweet in useful_tweets:
        tweet_text = tweet['text']
        tokens = nltk.word_tokenize(tweet_text)
        bgs = nltk.bigrams(tokens)
        for name in bgs:
            if name[0][0].isupper() and name[1][0].isupper():
                if name in result:
                    result[name] += 1
                else:
                    result[name] = 1
    target.hosts = sorted(result, key=result.get, reverse=True)[0:2]
    return