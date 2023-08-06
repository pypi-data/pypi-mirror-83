from scipy.signal import sawtooth as sawtooth
from .Wave import Wave
from ..utils import plot_2D


class Sawtooth(Wave):
    def __init__(self,
                 amplitude: float = 1,
                 period: float = 1,
                 offsets: tuple = (0, 0),
                 resolution: int = 1000):
        super().__init__(sawtooth, amplitude, period, offsets, 0, resolution)
        self.anim.x_args = [None, False, None, False]
        self.anim.y_args = [1]
        self.anim.default_speed = 0.02

    def plot(self,
             periods: float = 1,
             line_width: float = 1):
        x = self.generate_x(periods=periods, linspace=False)
        y = self.generate_y(x, period_constant=1)

        plot_2D(x, y, line_width)
