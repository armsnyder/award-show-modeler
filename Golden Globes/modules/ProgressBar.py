# Adds and manages a progress bar in the terminal

import sys


class ProgressBar:

    def __init__(self, title, total_x):
        self.title = title
        self.progress_x = 0
        self.total_x = total_x
        self.total_length = 40
        self.set_progress(0)
        self.running = True
        return

    def set_progress(self, x):
        self.progress_x = x
        self.display_progress()

    def display_progress(self):
        bar_length = int(self.progress_x * self.total_length // self.total_x)
        text = '\r' + self.title + ': [' + '#'*bar_length + '-'*(self.total_length - bar_length) + ']'
        sys.stdout.write(text)
        sys.stdout.flush()
        if self.total_x == self.progress_x:
            self.end_progress()

    def end_progress(self):
        if self.running:
            print ''
        self.running = False