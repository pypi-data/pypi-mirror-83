"""Main module."""
from datetime import datetime
from dnd_dice.dices import *


def start_dnd_shell(name):
    log = LogFile(name)
    shell = DnDShell(log)
    shell.start()


class LogFile():
    """
    Simple logger for DnD shell session
    """

    __date_format = '%Y-%m-%d %H:%M:%S'


    def __init__(self, name):
        self.__file_name = f'{name}-{datetime.now().strftime(self.__date_format)}'
        with open(self.__file_name, 'w') as file:
            file.write(f'DnD Dice Log\nStarted at: {datetime.now().strftime(self.__date_format)}\n---\n')


    def add_log(self, result):
        with open(self.__file_name, 'a') as file:
            file.write(f'\n{datetime.now().strftime(self.__date_format)}')


class DnDShell():
    __DICES = {
        '4': D4Dice(),
        '6': D6Dice(),
        '8': D8Dice(),
        '10': D10Dice(),
        '12': D12Dice(),
        '20': D20Dice(),
    }

    def __init__(self, logger):
        self.__logger = logger


    def start(self):
        running = True
        while running:
            print('[DnD] >> ', end='')
            dice_throw = input()
            if dice_throw == '':
                continue
            if dice_throw == 'exit':
                running = False
                continue
            arguments = [a for a in dice_throw.split(' ') if a != '']
            print(arguments)
            for arg in arguments:
                q, d = arg.split('d')
                if str(d) not in self.__DICES:
                    continue
                dice = self.__DICES[d]
                for i in range(int(q)):
                    print(f'{dice.name} - {dice.throw_dice()}')

