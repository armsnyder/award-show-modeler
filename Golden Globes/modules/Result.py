# Stores the final results in whatever form we choose and defines functions to interpret results


class Result:
    def __init__(self):
        self.show_name = 'Golden Globes'
        self.hosts = {}
        self.winners = {}
        self.awards = {}
        self.presenters = {}
        self.nominees = {}

        self.start_time = {}
        self.daylight_savings = 0

    def print_results(self):
        print 'Hosts: %s and %s!' % (self.join_name(self.hosts[0]), self.join_name(self.hosts[1]))
        print self.hosts
        return

    def join_name(self, name):
        return name[0] + ' ' + name[1]