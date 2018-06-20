import matplotlib
import matplotlib.animation as animation
from matplotlib import colors

from event_ca import EventCA

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


class ViewIterator:
    def __init__(self):
        self.value = 0


def show_simulation(model, iterations=20, interval=100):
    cmap = colors.ListedColormap(['white', 'black'])
    fig = plt.figure()

    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)

    grid = plt.imshow(model.state, interpolation='nearest', cmap=cmap)
    ani = animation.FuncAnimation(fig, update_simple, fargs=(grid, model,),
                                  frames=iterations, interval=interval, repeat=False)

    plt.show()


def update_simple(i, grid, model):
    model.next_state()
    grid.set_data(model.state)

    return grid,


def show_event_simulation(model, iterations=20, interval=100):
    cmap = colors.ListedColormap(['white', 'grey', 'black'])
    fig = plt.figure()

    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)

    grid = plt.imshow(model.state, interpolation='nearest', cmap=cmap)

    it = ViewIterator()
    ani = animation.FuncAnimation(fig, update_event, fargs=(grid, model, it,),
                                  frames=iterations, interval=interval, repeat=False)

    plt.show()


def update_event(i, grid, model, iterator):
    model.next_event_queue()
    if iterator.value % 2 == 0:
        grid.set_data(ca.cells_for_view())
    else:
        model.execute_events()

        grid.set_data(ca.state)

    iterator.value += 1
    return grid,


def save_anim_as_gif(name, anim,
                     path_to_imagemagick='C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe'):
    matplotlib.rcParams['animation.convert_path'] = path_to_imagemagick
    anim.save(name, writer='imagemagick', fps=60, bitrate=-1)


ca = EventCA(30, True)
show_event_simulation(ca, 100, 555)
