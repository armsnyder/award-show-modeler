# Stores the final results in whatever form we choose and defines functions to interpret results

# Results that are already filled in are optional. We can make processes to extract them later if we're feeling
# ambitious.

import datetime
import json
import os
import util

import regex


class Result:
    def __init__(self):
        self.show_name = 'Golden Globes'
        self.start_time = None
        self.hosts = []
        self.winners = []
        self.presenters = {}
        self.nominees = {}
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
        return

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
                # 'year': self.start_time.strftime("%Y"),
                'year': 2013,
                'hosts': {
                    'method': 'detected',
                    'method_description': 'The tweets are filtered first by the regex \'hosts\' and second '
                                          'by a regex we wrote to extract names. These names are placed into '
                                          'a dictionary, which maintains the popularity of each name. The '
                                          'names are sorted by popularity, and the ones that are most often '
                                          'mentioned are returned.'
                },
                'nominees': {
                    'method': 'detected',
                    'method_description': ''
                },
                'awards': {
                    'method': 'detected',
                    'method_description': ''
                },
                'presenters': {
                    'method': 'detected',
                    'method_description': ''
                }
            },
            'data': {
                'unstructured': {
                    'hosts': self.hosts,
                    'winners': [winner for winner, award, time in self.winners],
                    'awards': [award for winner, award, time in self.winners],
                    'presenters': [],
                    'nominees': []
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