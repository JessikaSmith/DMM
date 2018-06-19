from itertools import chain

import numpy as np


class Environment:
    def __init__(self, size, random_init=False):
        self.size = size
        self.state = [[Cell()] * self.size for _ in range(self.size)]

        if random_init:
            self.init_random_state()

    def init_random_state(self):
        for cell in chain.from_iterable(zip(*self.state)):
            cell.init_random()

    def next_state(self):
        pass


class Cell:
    def __init__(self):
        # 0 - death, 1 - living
        self.value = 0

    def init_random(self):
        self.value = np.random.randint(2)

    def check(self):
        pass


env = Environment(10, True)
