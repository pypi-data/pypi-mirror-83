import matplotlib.pyplot as plt
import numpy as np
from .waves import Wave


def __lcm__(a, b):
    from fractions import gcd
    return a * b / gcd(a, b)


def _check_type(other):
    return Wave.Wave in type(other).__bases__ or type(other) is Wave.Wave


def x_range(minimum: float,
            maximum: float):
    plt.xlim(minimum, maximum)


def y_range(minimum: float,
            maximum: float):
    plt.ylim(minimum, maximum)


def view_axes(view: bool):
    plt.axis("on" if view else "off")


def center_axes():
    fig, ax = plt.gcf(), plt.gca()

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def left_axes():
    fig, ax = plt.gcf(), plt.gca()

    ax.spines['left'].set_position(('outward', 0))
    ax.spines['bottom'].set_position(('outward', 0))

    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_visible(True)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def dampen(decay_constant, x):
    return x * np.exp(-1 * decay_constant * x)


def plot_2D(x: np.ndarray,
            y: np.ndarray,
            line_width: float):
    plt.plot(x, y, linewidth=line_width)
    plt.show()
