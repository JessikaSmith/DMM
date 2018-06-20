from collections import Counter

import numpy as np

HOOD = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class EventCA:
    def __init__(self, size, random_init=False):
        self.size = size
        self.state = np.zeros((size, size))
        self.living = []
        self.queue = []
        if random_init:
            self.init_random_state()

        self.update_living()

    def init_random_state(self):
        self.state = np.random.randint(2, size=(self.size, self.size))

    def update_living(self):
        i, j = np.where(self.state == 1)
        self.living = sorted(list(zip(i, j)))

        print(len(self.living))

    def next_event_queue(self):
        cells = self.cells_to_check()

        for x, y in cells:
            # generate view event
            self.queue.append(Event("view", (x, y)))
            new_value = self.recalculate_cell(x, y)
            if self.state[x, y] != new_value:
                # generate change event
                self.queue.append(Event("change", (x, y), self.state[x, y], new_value))

    def execute_events(self):

        cnt = Counter()
        for event in self.queue:
            cnt[event.type] += 1
            x, y = event.cell
            if event.type == "view":
                continue
                # print("View event for cell: (%d, %d)" % (x, y))
            elif event.type == "change":
                # print("Change event for cell: (%d, %d) %d => %d" % (
                #     x, y, event.old_value, event.new_value))

                self.state[x, y] = event.new_value
        print(cnt)
        self.queue.clear()
        self.update_living()

    def cells_for_view(self):
        view_matrix = np.zeros((self.size, self.size))

        view_events = [e for e in self.queue if e.type == "view"]

        for event in view_events:
            x, y = event.cell
            view_matrix[x, y] = 0.5

        return view_matrix

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


class Event:
    def __init__(self, type, cell, old_value=-1, new_value=-1):
        self.type = type
        self.cell = cell
        self.old_value = old_value
        self.new_value = new_value

# ca = EventCA(10, True)
# ca.next_event_queue()
# print(ca.cells_for_view())
# ca.execute_events()
