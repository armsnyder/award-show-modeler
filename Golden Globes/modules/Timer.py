import datetime


class Timer:
    def __init__(self, name):
        self.name = name
        self.start = datetime.datetime.now()
        return

    def tic(self):
        self.start = datetime.datetime.now()

    def toc(self):
        now = datetime.datetime.now()
        difference = now - self.start
        print '%s: %d ms elapsed' % (self.name, difference.microseconds/1000)
        self.tic()