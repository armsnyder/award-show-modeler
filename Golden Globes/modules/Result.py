# Stores the final results in whatever form we choose and defines functions to interpret results

# Results that are already filled in are optional. We can make processes to extract them later if we're feeling
# ambitious.

import datetime
import json
import os
import util
import itertools

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
        return host_string

    def display_winners(self):
        """Not neally done....."""
        f = ''
        for winner, award, time in self.winners:
            f += winner + ': ' + award + ' at ' + time.strftime("%H:%M:%S") + '\n'
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
                'year': self.start_time.strftime("%Y"),
                'names': {
                    'hosts': {
                        'method': 'detected',
                        'method_description': 'The tweets are filtered first by the regex \'hosts\' and second \n'
                                              'by a regex we wrote to extract names. These names are placed into \n'
                                              'a dictionary, which maintains the popularity of each name. The \n'
                                              'names are sorted by popularity, and the ones that are most often \n'
                                              'mentioned are returned.'
                    },
                    'nominees': {
                        'method': 'detected',
                        'method_description': ''
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
                        'method_description': ''
                    }
                },
                'mappings': {
                    'nominees': {
                        'method': 'detected',
                        'method_description': ''
                    },
                    'presenters': {
                        'method': 'detected',
                        'method_description': ''
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
        for i in range(len(self.winners)):
            self.autograder_result['data']['structured'][self.winners[i][1]] = {
                'nominees': list(self.nominees[i]),
                'winner': self.winners[i][0],
                'presenters': list(self.presenters[i])
            }

    def show_best_dressed(self):
        best_string = 'Best Dressed: '
        number_of_best = len(self.best_dressed)
        for name in range(number_of_best):
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
        number_of_worst = len(self.worst_dressed)
        for name in range(number_of_worst):
            worst_string += self.join_name(self.worst_dressed[name])
            if name == number_of_worst-2:
                worst_string += ' and '
            elif name == number_of_worst-1:
                worst_string += '.'
            else:
                worst_string += ', '
        return worst_string