import numpy as np
import matplotlib
from matplotlib import colors
from cell import Cell

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# plt.interactive(True)

SIMULATION_TIME = 20

N = 20
matrix = np.zeros((N, N))
nums = [i for i in range(N)]
live_cells = dict()
cmap = colors.ListedColormap(['white', 'black'])
cmap_extended = colors.ListedColormap(['white', 'black', 'gray'])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.matshow(matrix, cmap=cmap)
ticks = [i + 0.5 for i in range(0, N - 1)]
plt.xticks(ticks)
plt.yticks(ticks)
ax.grid()


def onmouseclick(event):
    global live_cells
    y, x = int(round(event.xdata)), int(round(event.ydata))
    live_cells[x, y] = Cell([x, y], state=1)
    matrix[x, y] = 1
    ax.matshow(matrix, cmap=cmap)
    plt.xticks(ticks)
    plt.yticks(ticks)
    fig.canvas.draw()


def onkeypress(event):
    global live_cells
    neighborhood = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for _ in range(SIMULATION_TIME):
        new_cells_state = dict()
        matrix = np.zeros((N, N))
        for key in list(live_cells):
            # apply rule to the cell itself
            if recalculate_state(key, 1):
                new_cells_state[key[0], key[1]] = Cell([key[0], key[1]], state=1)
                matrix[key[0], key[1]] = 1
            #  working with neighborhood
            for mask in neighborhood:
                row = (key[0] + mask[0]) % N
                column = (key[1] + mask[1]) % N
                if recalculate_state((row, column), 0):
                    new_cells_state[row, column] = Cell([row, column], state=1)
                    matrix[row, column] = 1
        ax.matshow(matrix, cmap=cmap)
        plt.xticks(ticks)
        plt.yticks(ticks)
        fig.canvas.draw()
        live_cells = new_cells_state


def recalculate_state(coord, state):
    neighborhood = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    amount_of_alive_tees = 0
    for mask in neighborhood:
        row = coord[0] + mask[0]
        column = coord[1] + mask[1]
        if (row % N, column % N) in live_cells:
            amount_of_alive_tees += 1
    if state and (amount_of_alive_tees > 3 or amount_of_alive_tees < 2):
        return 0
    if not state and amount_of_alive_tees == 3:
        return 1
    return state


fig.canvas.mpl_connect('button_press_event', onmouseclick)
fig.canvas.mpl_connect('key_press_event', onkeypress)

plt.show()
