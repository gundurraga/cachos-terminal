import random


class Dice:
    def __init__(self):
        self._value = 1

    @property
    def value(self):
        return self._value

    def roll(self):
        self._value = random.randint(1, 6)
        return self._value

    def __str__(self):
        return f"Dice(value={self._value})"

    def __repr__(self):
        return self.__str__()
