import random


class Dice():
    def throw_dice(self):
        if self.index is None:
            raise Exception("Dice not implemented")
        return random.randint(1,self.index)


class D4Dice(Dice):
    def __init__(self):
        self.index = 4
        self.name = "D4"


class D6Dice(Dice):
    def __init__(self):
        self.index = 6
        self.name = "D6"


class D8Dice(Dice):
    def __init__(self):
        self.index = 8
        self.name = "D8"


class D10Dice(Dice):
    def __init__(self):
        self.index = 10
        self.name = "D10"


class D12Dice(Dice):
    def __init__(self):
        self.index = 12
        self.name = "D12"


class D20Dice(Dice):
    def __init__(self):
        self.index = 20
        self.name = "D20"
