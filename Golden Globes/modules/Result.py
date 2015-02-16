# Stores the final results in whatever form we choose and defines functions to interpret results

# Results that are already filled in are optional. We can make processes to extract them later if we're feeling
# ambitious.

import datetime

class Result:
    def __init__(self):
        self.show_name = 'Golden Globes'
        self.start_time = None
        self.hosts = []
        self.winners = []
        self.presenters = {}
        self.nominees = {}

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

    @staticmethod
    def join_name(name):
        return name[0] + ' ' + name[1]

    def hosts_string(self):
        host_string = 'Hosts: '
        number_of_hosts = len(self.hosts)
        for i in range(number_of_hosts):
            host_string += self.join_name(self.hosts[i])
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