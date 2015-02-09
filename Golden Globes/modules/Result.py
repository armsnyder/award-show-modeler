# Stores the final results in whatever form we choose and defines functions to interpret results

# Results that are already filled in are optional. We can make processes to extract them later if we're feeling
# ambitious.


class Result:
    def __init__(self):
        self.show_name = 'Golden Globes'
        self.categories = [
            'Best Motion Picture - Drama',
            'Best Motion Picture - Musical or Comedy',
            'Best Director',
            'Best Actor - Motion Picture Drama',
            'Best Actor - Motion Picture Musical or Comedy',
            'Best Actress - Motion Picture Drama',
            'Best Actress - Motion Picture Musical or Comedy',
            'Best Supporting Actor - Motion Picture',
            'Best Supporting Actress - Motion Picture',
            'Best Screenplay',
            'Best Original Score',
            'Best Original Song',
            'Best Foreign Language Film',
            'Best Animated Feature Film',
            'Cecil B. DeMille Award for Lifetime Achievement in Motion Pictures'
        ]
        self.start_time = None
        self.hosts = []
        self.winning_films = {}
        self.winning_people = {}
        self.presenters = {}
        self.nominees = {}

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