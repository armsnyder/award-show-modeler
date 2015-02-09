# Stores the final results in whatever form we choose and defines functions to interpret results


class Result:
    def __init__(self):
        self.show_name = 'Golden Globes'
        self.hosts = []
        self.winners = {}
        self.awards = {}
        self.presenters = {}
        self.nominees = {}
        self.start_time = {}

    def print_results(self):
        print ''
        print '*************************'
        print '||       RESULTS       ||'
        print '*************************'
        print self.hosts_string()
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