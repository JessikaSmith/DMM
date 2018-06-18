import numpy as np

HOOD = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class SimpleCA:
    def __init__(self, size, random_init=False):
        self.size = size
        self.state = np.zeros((size, size))
        self.living = []

        if random_init:
            self.init_random_state()

        self.update_living()

    def init_random_state(self):
        self.state = np.random.randint(2, size=(self.size, self.size))

    def update_living(self):
        i, j = np.where(self.state == 1)
        self.living = sorted(list(zip(i, j)))

    def next_state(self):
        cells_to_check = list(self.living)
        # add all neibs of the living cells
        for cell in self.living:
            for nb in HOOD:
                idx = ((cell[0] + nb[0]) % self.size, (cell[1] + nb[1]) % self.size)
                if idx not in cells_to_check:
                    cells_to_check.append(idx)

        new_state = np.copy(self.state)

        for x, y in cells_to_check:
            new_state[x, y] = self.recalculate_cell(x, y)

        self.state = new_state
        self.update_living()

    def recalculate_cell(self, x, y):
        hood_indices = [[], []]
        for nb in HOOD:
            hood_indices[0].append((x + nb[0]) % self.size)
            hood_indices[1].append((y + nb[1]) % self.size)
        hood_sum = np.sum(self.state[hood_indices])

        if self.state[x, y] and (hood_sum > 3 or hood_sum < 2):
            return 0
        if not self.state[x, y] and hood_sum == 3:
            return 1

        return self.state[x, y]


ca = SimpleCA(10, True)

for _ in range(100):
    ca.next_state()
