import matplotlib
import matplotlib.animation as animation
from matplotlib import colors

from simple_ca import SimpleCA

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


def show_simulation(model, iterations=20, interval=100):
    cmap = colors.ListedColormap(['white', 'black'])
    fig = plt.figure()

    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)

    grid = plt.imshow(model.state, interpolation='nearest', cmap=cmap)
    ani = animation.FuncAnimation(fig, update, fargs=(grid,),
                                  frames=iterations, interval=interval, repeat=False)

    plt.show()


def update(i, grid):
    ca.next_state()
    grid.set_data(ca.state)

    return grid,


def save_anim_as_gif(name, anim,
                     path_to_imagemagick='C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe'):
    matplotlib.rcParams['animation.convert_path'] = path_to_imagemagick
    anim.save(name, writer='imagemagick', fps=60, bitrate=-1)


ca = SimpleCA(30, True)
show_simulation(ca, 30, 30)
