import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Animator:
    def __init__(self, amplitude, default_speed, x_func, y_func, x_args, y_args):
        self.func = None
        self.fig, self.ax = None, None
        self.amplitude = amplitude
        self.default_speed = default_speed
        self.line = None
        self.x_func = x_func
        self.y_func = y_func
        self.x_args = x_args
        self.y_args = y_args

    def animate(self,
                speed: float = 1,
                line_width: float = 1):

        speed *= self.default_speed
        self.fig = plt.gcf()
        self.ax = plt.gca()
        self.ax.set_ylim([-self.amplitude, self.amplitude])

        def get_x_y(i):
            x = self.x_func(self.x_args[0], self.x_args[1], self.x_args[2], self.x_args[3])
            y = self.y_func(x + (speed * i), self.y_args[0])
            return x, y

        def init():
            self.ax.clear()
            self.line, = self.ax.plot([], [], lw=line_width)
            self.line.set_data([], [])

            x = self.x_func(start_at_0=self.x_args[3])
            y = self.y_func(self.x_func(100), self.y_args[0])
            x_min, y_min = np.amin(x), np.amin(y)
            x_max, y_max = np.amax(x), np.amax(y)
            dx, dy = (x_max - x_min), (y_max - y_min)
            self.ax.set_xlim([x_min - (dx * .1), x_max + (dx * .1)])
            self.ax.set_ylim([y_min - (dy * .1), y_max + (dy * .1)])

            return self.line,

        def update(i):
            x, y = get_x_y(i)
            self.line.set_data(x, y)
            return self.line,

        anim = FuncAnimation(self.fig, update, init_func=init,
                             interval=17, blit=True)

        plt.show()
