import numpy as np
import matplotlib
from matplotlib import colors

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.interactive(True)

cmap = colors.ListedColormap(['white', 'black'])
cmap_extended = colors.ListedColormap(['white', 'black', 'gray'])


class Grid:

    def __init__(self, n):
        self.n = n
        self.matrix = np.zeros((n, n))
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ticks = [i + 0.5 for i in range(0, self.n - 1)]
        self.initial_configuration()

    def onmouseclick(self, event):
        x, y = int(round(event.xdata)), int(round(event.ydata))
        self.matrix[y, x] = 1
        self.ax.matshow(self.matrix, cmap=cmap)
        plt.xticks(self.ticks)
        plt.yticks(self.ticks)
        self.fig.canvas.draw()

    def onkeypress(self, event):

        print(self.matrix)
        if (self.matrix[0, 0] == 0):
            self.matrix[0, 0] = 1
        else:
            self.matrix[0, 0] = 0
        self.ax.matshow(self.matrix, cmap=cmap)
        plt.xticks(self.ticks)
        plt.yticks(self.ticks)
        self.fig.canvas.draw()

    def initial_configuration(self):
        self.ax.matshow(self.matrix, cmap=cmap)
        plt.xticks(self.ticks)
        plt.yticks(self.ticks)
        self.ax.grid()
        self.fig.canvas.mpl_connect('button_press_event', self.onmouseclick)
        self.fig.canvas.mpl_connect('key_press_event', self.onkeypress)
