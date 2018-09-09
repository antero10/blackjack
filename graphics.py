import os
import sys
import time
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format

class Graphics(object):

    def __init__(self):
        pass

    def clearScreen(self):
        os.system('cls') # on windows
        os.system('clear') #

    def getSizeOfWindow(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        return rows, columns

    def render(self):
        pass

    def renderTitle(self, text):
        print(os.linesep) # just a blank line
        print('*****' * 10)
        print('%s' % text.upper())
        print('*****' * 10)

    def renderList(self, options):
        print(os.linesep) # just a blank line
        for option in options:
            print(option + '\t')
        try:
            return int(raw_input('Select Option:' + os.linesep))
        except ValueError:
            pass

    def fullScreenText(self, text):
        print(os.linesep) # just a blank line
        print(os.linesep) # just a blank line
        os.system('cls' if os.name == 'nt' else 'clear')
        init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
        cprint(figlet_format(text, font='starwars'),
               'yellow', attrs=['bold'])

    def renderScore(self):
        pass

    def getValueInput(self, text):
        return raw_input(text + os.linesep)
