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

    def insert_pattern(self, pattern, x_offset=0, y_offset=0):

        if x_offset + pattern.shape[0] < self.size and y_offset + pattern.shape[1] < self.size:
            self.state = np.zeros((self.size, self.size))
            self.state[x_offset:x_offset + pattern.shape[0], y_offset:y_offset + pattern.shape[1]] = pattern

            self.update_living()
        else:
            raise ValueError('Grid size does not correspond to pattern size')

    def next_state(self):

        new_state = np.copy(self.state)
        cells = self.cells_to_check()

        for x, y in cells:
            new_state[x, y] = self.recalculate_cell(x, y)

        self.state = new_state
        self.update_living()

    def cells_to_check(self):
        cells_to_check = list(self.living)
        # add all neibs of the living cells
        for cell in self.living:
            for nb in HOOD:
                idx = ((cell[0] + nb[0]) % self.size, (cell[1] + nb[1]) % self.size)
                if idx not in cells_to_check:
                    cells_to_check.append(idx)

        return cells_to_check

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


def cycle_length():
    ca = SimpleCA(10)
    ca.insert_pattern(generate_oscillator_figure(3))
    initial = np.copy(ca.state)
    ca.next_state()
    len = 1
    while not np.array_equal(initial, ca.state):
        ca.next_state()
        len += 1

    print("cycle was found with length: %d" % len)


def generate_static_figure(mode):
    f = open('figure_patterns/static/static_' + str(mode) + '.txt')
    figure = load_figure(f)

    return figure


def generate_oscillator_figure(mode):
    f = open('figure_patterns/oscillator/osc_' + str(mode) + '.txt')
    figure = load_figure(f)
    return figure


def generate_moving_figure(mode):
    f = open('figure_patterns/moving/moving_' + str(mode) + '.txt')
    figure = load_figure(f)
    return figure


def load_figure(file):
    x, y = map(int, file.readline().split())
    figure = np.zeros((y, x))
    for j in range(y):
        row = list(map(int, file.readline().split()))
        for i in range(len(row)):
            figure[j, i] = row[i]

    file.close()

    return figure
