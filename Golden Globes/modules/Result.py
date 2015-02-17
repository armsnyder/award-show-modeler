# Stores the final results in whatever form we choose and defines functions to interpret results

# Results that are already filled in are optional. We can make processes to extract them later if we're feeling
# ambitious.

import datetime
from GUI import *
import json
import os
import util
import itertools

import image_search
import GUI
import regex


class Result:
    def __init__(self):
        self.show_name = 'Golden Globes'
        self.start_time = None
        self.hosts = []
        self.winners = []
        self.presenters = []
        self.nominees = []
        self.best_dressed = []
        self.worst_dressed = []
        self.autograder_result = {}

    def print_results(self):
        print ''
        print '*************************'
        print '||       RESULTS       ||'
        print '*************************'
        print self.hosts_string()
        print ''
        print self.display_winners()
        print ''
        print self.show_best_dressed()
        print ''
        print self.show_worst_dressed()
        print ''
        return

    @staticmethod
    def join_name(name):
        return name[0] + ' ' + name[1]

    def hosts_string(self):
        host_string = 'Hosts: '
        number_of_hosts = len(self.hosts)
        for i in range(number_of_hosts):
            host_string += self.hosts[i]
            if i == number_of_hosts-2:
                host_string += ' and '
            elif i == number_of_hosts-1:
                host_string += '!'
            else:
                host_string == ', '

        GUI.html_hosts(host_string)
        GUI.html_image_add(host_string)
        return host_string

    def display_winners(self):
        """Not neally done....."""
        f = ''
        for winner, award, time in self.winners:
            f += winner + ': ' + award + ' at ' + datetime.datetime.fromtimestamp(time).strftime("%H:%M:%S") + '\n'
        return f

    def print_output_file(self):
        output_dir = util.get_path(util.output_path)
        if not self.autograder_result:
            self.compile_autograder_result()
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        files_nums_in_dest = []
        file_num = 0
        for f in os.listdir(output_dir):
            if os.path.isfile(os.path.join(output_dir, f)):
                match = regex.output.search(f)
                if match:
                    files_nums_in_dest.append(int(match.group(1)))
        for i in range(1, 99):
            if i not in files_nums_in_dest:
                file_num = i
                break
        f_o_name = 'output_' + str(file_num) + '.json'
        f_o_path = os.path.join(output_dir, f_o_name)
        with open(f_o_path, 'w') as f_o:
            json.dump(self.autograder_result, f_o)
        return os.path.abspath(str(f_o_path))

    def compile_autograder_result(self):
        self.autograder_result = {
            'metadata': {
                'year': datetime.datetime.fromtimestamp(self.start_time).strftime("%Y"),
                'names': {
                    'hosts': {
                        'method': 'detected',
                        'method_description': 'The tweets are filtered first by the regex \'host\' and second by \n'
                                              'a regex we wrote to extract names. These names are placed into a \n'
                                              'dictionary, which maintains the popularity of each name. The \n'
                                              'names are sorted by popularity, and the ones that are most often \n'
                                              'mentioned are returned.'
                    },
                    'nominees': {
                        'method': 'detected',
                        'method_description': 'For every award, an estimated time of conferral is used as an \n'
                                              'anchor time to collect a cursor of tweets which are matched first \n'
                                              'to the regex \'nominees\' and \n then to the regex for names to \n'
                                              'extract probable nominees. The most popular names that are not \n'
                                              'hosts or winners are selected.'
                    },
                    'awards': {
                        'method': 'detected',
                        'method_description': 'The awards are detected in conjunction with the winners. First, \n'
                                              'the tweets are filtered by a regex that checks if the tweet \n'
                                              'contains a form of the word \'win\' and \'best\'. These tweets \n'
                                              'are further filtered by removing those using subjunctive tense \n'
                                              'or occurring before the ceremony\'s start time, which is also \n'
                                              'detected. The remaining tweets are matched against several \n'
                                              'language models that attempt to pull out winner and award names. \n'
                                              'The awards are grouped by winner (as the dictionary key), which \n'
                                              'goes through a couple consolidation steps. The top winners are \n'
                                              'extracted, and the most popular award name per winner bin is \n'
                                              'added to the award list.'
                    },
                    'presenters': {
                        'method': 'detected',
                        'method_description': 'Detected at the same time as nominees, the regex generator for time \n'
                                              'ranges is used to match a cursor of tweets from just before a \n'
                                              'certain award is conferred. Those tweets are matched with the regex \n'
                                              'for names, and the most popular names who are not winners are returned.'
                    }
                },
                'mappings': {
                    'nominees': {
                        'method': 'detected',
                        'method_description': 'Both nominees and presenters are mapped to their awards by \n'
                                              'maintaining the timestamps on tweets throughout the program. \n'
                                              'We are thus able to detect when an award was given. These times \n'
                                              'are passed into a function that procedurally generates regular \n'
                                              'expressions that match tweets that were tweeted around a certain \n'
                                              'time. We look at a window of 6 minutes after a winner is \n'
                                              'announced for the nominees and map the results to the winner\'s \n'
                                              'award.'
                    },
                    'presenters': {
                        'method': 'detected',
                        'method_description': 'Same as nominees, but with a window of 3 minutes before an award \n'
                                              'is announced.'
                    }
                }
            },
            'data': {
                'unstructured': {
                    'hosts': self.hosts,
                    'winners': [winner for winner, award, time in self.winners],
                    'awards': [award for winner, award, time in self.winners],
                    'presenters': list(itertools.chain.from_iterable(self.presenters)),
                    'nominees': list(itertools.chain.from_iterable(self.nominees))
                },
                'structured': {}
            }
        }

        # Structured
        for winner, award, time in self.winners:
            self.autograder_result['data']['structured'][award] = {
                'nominees': [],
                'winner': winner,
                'presenters': []
            }

        for winner, award, time in self.winners:
            GUI.html_text_add(award)
            GUI.html_text_winner(winner)
            GUI.html_image_add(image_search.find_image(winner))
            GUI.html_text_time(datetime.datetime.fromtimestamp(time).strftime("%H:%M:%S"))

        html_done()
        for i in range(len(self.winners)):
            self.autograder_result['data']['structured'][self.winners[i][1]] = {
                'nominees': list(self.nominees[i]),
                'winner': self.winners[i][0],
                'presenters': list(self.presenters[i])
            }

    def show_best_dressed(self):
        best_string = 'Best Dressed: '
        GUI.html_text_heading(best_string)
        number_of_best = len(self.best_dressed)
        for name in range(number_of_best):
            # GUI.html_text_add(name)
            # GUI.html_image_add(name)
            best_string += self.join_name(self.best_dressed[name])
            if name == number_of_best-2:
                best_string += ' and '
            elif name == number_of_best-1:
                best_string += '.'
            else:
                best_string += ', '
        return best_string

    def show_worst_dressed(self):
        worst_string = 'Worst Dressed: '
        GUI.html_text_heading(worst_string)
        number_of_worst = len(self.worst_dressed)
        for name in range(number_of_worst):
            # GUI.html_text_add(name)
            # GUI.html_image_add(name)
            worst_string += self.join_name(self.worst_dressed[name])
            if name == number_of_worst-2:
                worst_string += ' and '
            elif name == number_of_worst-1:
                worst_string += '.'
            else:
                worst_string += ', '
        return worst_string