import json
import sys
from nltk.metrics import edit_distance,masi_distance
import difflib
from collections import Counter
from pprint import pprint
import os

decision_to_methods = {'1': 'hardcoded', '2': 'scraped', '3': 'detected'}
methods_to_decision = {'hardcoded': 1, 'scraped': 2, 'detected': 3}

def acceptable_distance(resultlen,matchlen):
    minlen = float(min(resultlen,matchlen))
    return (minlen/2.0 + float(max(resultlen,matchlen)-minlen))

def prep(word):
    return word.replace('tv','television').replace('/',' or ').replace('movie','motion picture').replace('film','motion picture').replace('show','series').strip().lower()

def norm_text(textlist):
    """Takes a list of text and returns a string of normalized text."""
    textlist = [' '.join(line.lower().split()) for line in textlist]
    textlist = ["".join([c for c in line if c.isalnum() or c.isspace()]) for line in textlist]
    text = '\n'.join(textlist)

    return text

def text(result,answer):
    """Accepts two normalized texts, as output by the norm_text function, and returns a score based on the match length relative to the longest text length."""
    len_result = len(result)
    len_answer = len(answer)

    if (result in answer) or (answer in result):
        textscore = min(len_result,len_answer)/float(max(len_result,len_answer))
    else:
        s = difflib.SequenceMatcher(None, result, answer)

    # matchlen = len('\n'.join([newtext[m[0]:m[0]+m[2]].strip() for m in s.get_matching_blocks() if m[2] > 1]).strip().split())
    # textscore = float(matchlen)/min([len(oldtext.strip().split()),len(newtext.strip().split())])
        longest = s.find_longest_match(0,len_result,0,len_answer)
        longest = longest.size/float(max(len_result,len_answer))
        if longest > 0.3:
            matchlen = sum([m[2] for m in s.get_matching_blocks() if m[2] > 1])
            textscore = float(matchlen)/max(len_result,len_answer)
        else:
            textscore = longest

    return textscore

def calc_awards(result,answer):
    translation = {}
    problems = []
    for r in result:
        prepped = prep(r)
        rlist = set(prepped.split())
        if 'animated' in rlist:
            translation[r] = 'best animated feature film'
        elif 'foreign' in rlist:
            translation[r] = 'best foreign language film'
        elif 'director' in rlist:
            translation[r] = 'best director - motion picture'
        elif rlist.intersection(('screenplay', 'script')):
            translation[r] = 'best screenplay - motion picture'
        elif 'score' in rlist:
            translation[r] = 'best original score - motion picture'
        elif 'song' in rlist:
            translation[r] = 'best original song - motion picture'
        elif rlist.intersection(('cecil','demille')):
            translation[r] = 'cecil b. demille award'
        else:
            if rlist.intersection(('comedy','musical')):
                qualifier = 'comedy or musical'
            elif 'drama' in rlist:
                qualifier = 'drama'
            else:
                qualifier = None

            if rlist.intersection(('performance','actor','actress','supporting')):
                if 'actor' in rlist:
                    actor = 'actor'
                elif 'actress' in rlist:
                    actor = 'actress'
                else:
                    actor = None

                if rlist.intersection(('miniseries','mini-series')) or (True in [phrase in prepped for phrase in ['mini series', 'made for television', 'television motion picture']]):
                    if qualifier:
                        problems.append(r)
                    elif 'supporting' in rlist:
                        if actor:
                            translation[r] = 'best performance by an %s in a supporting role in a series, mini-series or motion picture made for television'%actor
                        else:
                            problems.append(r)
                    elif actor:
                        translation[r] = 'best performance by an %s in a mini-series or motion picture made for television'%actor
                    else:
                        problems.append(r)
                elif 'television' in rlist:
                    if not qualifier:
                        problems.append(r)
                    elif actor:
                        translation[r] = 'best performance by an %s in a television series - %s'%(actor,qualifier)
                    else:
                        problems.append(r)
                elif rlist.intersection(('motion','picture')):
                    if not actor:
                        problems.append(r)
                    elif 'supporting' in rlist:
                        if qualifier:
                            problems.append(r)
                        else:
                            translation[r] = 'best performance by an %s in a supporting role in a motion picture'%actor
                    elif qualifier:
                        translation[r] = 'best performance by an %s in a motion picture - %s'%(actor,qualifier)
                    else:
                        problems.append(r)
                else:
                    problems.append(r)
            elif rlist.intersection(('miniseries','mini-series')) or (True in [phrase in prepped for phrase in ['mini series', 'made for television', 'television motion picture']]):
                if qualifier:
                    problems.append(r)
                else:
                    translation[r] = 'best mini-series or motion picture made for television'
            elif 'television series' in prepped:
                if qualifier:
                    translation[r] = 'best television series - %s'%qualifier
                else:
                    problems.append(r)
            elif 'motion picture' in prepped:
                if qualifier:
                    translation[r] = 'best motion picture - %s'%qualifier
                else:
                    problems.append(r)
            else:
                problems.append(r)
    if len(problems) > 0:
        print "Could not find a match for:"
    for p in problems:
        print p
    # sum([edit_distance(t,translation[t])/float(max(len(t),len(translation[t]))) for t in translation])

    return translation, len(translation)

def calc_translation(result,answer):
    translation = {}
    new_intersection = 0
    score_by_results = {}
    score_by_answers = {}
    for r in result:
        score_by_results[r] = Counter()
        for a in answer:
            if a not in score_by_answers:
                score_by_answers[a] = Counter()
            score_by_results[r][a] = text(norm_text([a]),norm_text([r]))
            score_by_answers[a][r] = score_by_results[r][a]
    for r in score_by_results:
        cnt = 0
        ranking = score_by_results[r].most_common()
        flag = True
        while flag:
            answer_match = ranking[cnt][0]
            max_result = score_by_answers[answer_match].most_common()[0]
            # print "result: %s\tbest answer: %s, %.1f\tbest result for answer: %s, %.2f"%(r,answer_match,score_by_results[r][answer_match],max_result[0], max_result[1])
            # max_length = acceptable_distance(len(answer_match),len(r))
            # print "result: %s\tmatch: %s\tdistance: %f\tdistance to alt: %f\tmax distance: %f"%(r,answer_match,score_by_results[r][answer_match],min_result[1],max_length)

            if score_by_results[r][answer_match] < 0.45:
                # print "No result found."
                flag = False
            elif (max_result[0] == r) or (score_by_results[r][answer_match] > score_by_answers[answer_match][max_result[0]]):
                translation[r] = answer_match
                change = score_by_results[r][answer_match]
                # print "%s\t->\t%s:\t%f\n"%(r,answer_match,change)
                new_intersection += change
                flag = False

            cnt += 1
            if cnt == len(ranking):
                # print "No result found.\n"
                flag = False
            
    return translation, new_intersection

def calc_score(result, answer, awds=False):
    """Accepts two lists of strings and returns a score for how
    closely they match, and a dictionary mapping result list items
    to their closest match in the answer list"""
    intersection = result.intersection(answer)
    len_intersection = len(intersection)
    len_union = len(result.union(answer))
    len_result = len(result)
    len_answer = len(answer)
    new_intersection = len_intersection

    translation = dict(zip(intersection,intersection))
    if len_result == len_answer and len_intersection == len_answer:
        m = 1.0
    elif len_intersection == len_result:
        # all results are correct but some are missing
        m = 0.95
        translation.update(dict(zip(answer-result,[""]*len(answer-result))))
    else:
        if awds:
            trans, new_intersection = calc_awards(result, answer)
        else:
            trans, new_intersection = calc_translation(result,answer)
        translation.update(trans)

        if len_intersection == len_answer:
            # correct results for entire answer list, but some extra
            # results as well
            m = 0.9
        else:
            new_result = set([translation[r] if r in translation else r for r in result])
            intersection = new_result.intersection(answer)
            len_intersection = len(intersection)
            len_union = len(new_result.union(answer))
            len_result = len(new_result)

            if len_result == len_answer and len_intersection == len_answer:
                m = 1.0
            elif len_intersection == len_result:
                # all results have a reasonable answer match but some are missing
                m = 0.95
            elif len_intersection == len_answer:
                # all answers have a reasonable result match, but there are
                # some extra results as well
                m = 0.9
            elif len_intersection > 0:
                # when we translate, there is some intersection.
                m = 0.85
            else:
                return 0, translation

        len_intersection = new_intersection

    return (len_intersection / float(len_union)) * m, translation

def check_metadata(item,metadata):
    if (item in metadata) and (metadata[item]['method'] == 'hardcoded'):
        print "The %s were hard coded.\n"%item
    else:
        print item
        print metadata[item]['method']
        print metadata[item]['method_description']
        print "\n1. Treat as hardcoded.\n2. Treat as scraped.\n3. Treat as detected."
        decision = raw_input()
        metadata[item]['method'] = decision_to_methods[decision]

    return metadata            

def lowercase(item):
    for i in item['unstructured']:
        item['unstructured'][i] = [a.lower() for a in item['unstructured'][i]]
    structured = {}
    for award in item['structured']:
        new_award = {}
        for info_type in item['structured'][award]:
            if info_type=='winner':
                new_award[info_type] = item['structured'][award][info_type].lower()
            else:
                new_award[info_type] = [i.lower() for i in item['structured'][award][info_type]]
        structured[award.lower()] = new_award
    item['structured'] = structured

    return item

def main(filename):
    with open(filename, 'r') as f:
        results = json.load(f)
    results['data'] = lowercase(results['data'])

    answer_key = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'gg%sanswers.json'%str(results['metadata']['year']))
    with open(answer_key,'r') as f:
        answers = lowercase(json.load(f))

    scores = {'unstructured': {},'structured': {}}
    translation = {}
    total = 0

    unstructuredstring = ""
    for item in results['data']['unstructured']:
        weight = len(answers['unstructured'][item])
        if item in results['metadata']:
            results['metadata'] = check_metadata(item, results['metadata'])
            weight = weight*(methods_to_decision[results['metadata'][item]['method']]-1.0)/2.0
        if weight != 0:
            score, trans = calc_score(set(results['data']['unstructured'][item]),set(answers['unstructured'][item]), item=="awards")
            translation.update(trans)
            scores['unstructured'][item] = weight*score
            unstructuredstring += "\n%.2f x %3.2f\t%s\n"%(score,weight,item)
        elif item == 'awards':
            trans, temp = calc_awards(set(results['data']['unstructured'][item]),set(answers['unstructured'][item]))
            translation.update(trans)
        total += weight
    pprint(translation)
    print "CALCULATING UNSTRUCTURED SCORES"
    print "=============================\n"
    print unstructuredstring
    scores['unstructured']['overall'] = sum(scores['unstructured'].values())
    scores['unstructured']['total'] = total
    print "-----------------------------"
    print "TOTAL\t%.2f / %.2f\n"%(scores['unstructured']['overall'],total)
    print "\n=============================\n"
    print "CALCULATING STRUCTURED SCORES"
    print "=============================\n"
    win_scores = []
    totals = {}

    for a in results['data']['structured']:
        if a in translation:
            translated = translation[a]
            print translated
            for item in results['data']['structured'][a]:
                if item in results['metadata']:
                    length = len(answers['structured'][translated][item])
                    weight = length*(methods_to_decision[results['metadata'][item]['method']]-1.0)/2.0
                    if weight != 0:
                        transitem = set([translation[r] if r in translation else r for r in results['data']['structured'][a][item]])
                        if length > 0:
                            score = (1 - masi_distance(set(answers['structured'][translated][item]),transitem))*length
                            if item not in scores['structured']:
                                scores['structured'][item] = score
                                totals[item] = length
                            else:
                                scores['structured'][item] += score
                                totals[item] += length
                            print "\t%s:\t%.2f / %d"%(item.capitalize(),score,length)
                elif item == "winner":
                    weight = 1
                    if results['data']['structured'][a]['winner'] in translation:
                        if results['data']['structured'][a]['winner'] and (answers['structured'][translated]['winner'] == translation[results['data']['structured'][a]['winner']]):
                            score = 1
                        else:
                            score = 0
                    else:
                        score = 0

                    win_scores.append(score)
                    print "\tWinner:\t%d"%score

    print "=============================\n"
    scores['structured']['winners'] = sum(win_scores)
    scores['structured']['overall'] = sum(scores['structured'].values())
    scores['structured']['total'] = sum([totals[item] for item in totals]) + len(win_scores)

    if 'nominees' in scores['structured']:
        print "Structured nominees score:  \t%.2f / %.2f"%(scores['structured']['nominees'], totals['nominees'])
    if 'presenters' in scores['structured']:
        print "Structured presenters score:\t%.2f / %.2f"%(scores['structured']['presenters'],totals['presenters'])
    print "Structured winners score:   \t%.2f / %.2f"%(scores['structured']['winners'],float(len(win_scores)))
    
    print "-----------------------------"
    print "TOTAL                       \t%.2f / %.2f\n"%(scores['structured']['overall'],scores['structured']['total'])
    print "\n=============================\n"
    print "CALCULATING TOTAL SCORES"
    print "=============================\n"

    scores['overall'] = scores['unstructured']['overall'] + scores['structured']['overall']
    scores['total'] = scores['unstructured']['total'] + scores['structured']['total']

    print "TOTAL\t%.2f / %.2f\n"%(scores['overall'],scores['total'])

    with open('gg%sscores.json'%str(results['metadata']['year']),'w') as f:
        json.dump(scores,f)

if __name__ == '__main__':
    main(sys.argv[1])