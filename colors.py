import sys


class ColorOutput(object):
    def __init__(self):
        self.prefix = '\u001b['
        self.reset = self.prefix + '0m'
        self.decorations = {
                '': '',
                'bold': self.prefix +'1m',
                'underline': self.prefix +'4m',
                'reversed': self.prefix +'7m'
                }

        self.colors = {
                '': '',
                'red': self.prefix +'31m',
                'green': self.prefix +'32m',
                'yellow': self.prefix +'33m',
                'blue': self.prefix +'34m',
                'magenta': self.prefix +'35m',
                'cyan' : self.prefix +'36m',
                'white': self.prefix +'37m',
                'b_red': self.prefix +'31;1m',
                'b_green': self.prefix +'32;1m',
                'b_yellow': self.prefix +'33;1m',
                'b_blue': self.prefix +'34;1m',
                'b_magenta': self.prefix +'35;1m',
                'b_cyan' : self.prefix +'36;1m',
                'b_white': self.prefix +'37;1m'
                }


    def write(self, text, color='', decoration=''):
        sys.stdout.write(self.decorations[decoration] + self.colors[color] + text + self.reset)


    def writeln(self, text, color='', decoration=''):
        self.write(text+'\n', color, decoration)
