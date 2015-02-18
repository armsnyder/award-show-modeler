import nltk
import operator

import regex
import util


def run(db, target, event):
    event.wait()
    util.vprint("Winners received. finding presenters and nominees...")
    for winner, value, time in target.winners:
        presenter_names = {}
        nominee_names = {}
        for i in [-1, 1]:
            if i == -1:
                current_dict = presenter_names
                start = time - 180000
                end = time
            else:
                current_dict = nominee_names
                start = time
                end = time + 360000
            cursor = db.collection.find({'timestamp_ms': {'$gt': str(start), '$lt': str(end)}})
            for tweet in cursor:
                if i == 1 and not regex.eehhhh.match(tweet['text']):
                    continue
                n = regex.name.match(tweet['text'])
                if n:
                    n = n.group()
                    n = n.lower()
                    toks = nltk.word_tokenize(n)
                    if toks[0] in util.common_words or toks[1] in util.common_words:
                        continue
                    else:
                        if n in current_dict:
                            current_dict[n] += 1
                        # elif not weed_out(n, target):
                        else:
                            current_dict[n] = 1
        pl = sorted(presenter_names.items(), key=operator.itemgetter(1), reverse=True)
        nl = sorted(nominee_names.items(), key=operator.itemgetter(1), reverse=True)
        if winner in pl:
            pl.remove(winner)
        if winner in nl:
            nl.remove(winner)

        if len(pl):
            pl_trunc = []
            for i in range(len(pl)):
                if i > 1:
                    break
            pl_trunc.append(pl[i][0])
            target.presenters.append(tuple(pl_trunc))
        else:
            target.presenters.append(())

        if len(nl):
            nl_trunc = []
            for j in range(len(nl)):
                if i > 3:
                    break
                nl_trunc.append(pl[j][0])
            target.nominees.append(tuple(nl_trunc))
        else:
            target.nominees.append(())
    util.vprint("Finished Presenters and Noms")
    return


def weed_out(name, target):
    # hits = ia.search_person(name)
    # if not hits:
    #     return True
    if name in target.hosts:
        return True
    if name in target.winning_people:
        return True
    return False
