import numpy as np
import warnings
from ..utils import __lcm__, dampen, plot_2D, _check_type
from ..Animator import Animator


class Wave:
    def __init__(self,
                 func,
                 amplitude: float = 1,
                 period: float = (2 * np.pi),
                 offsets: tuple = (0, 0),
                 decay_constant: float = 0,
                 resolution: int = 50):
        self.func = func
        self.amplitude = amplitude
        self.frequency = float(1 / self.amplitude) if amplitude != 0 else 0
        self.period = period
        self.offsets = offsets
        self.decay_constant = decay_constant
        self.resolution = resolution
        self.anim = Animator(self.amplitude,
                             0.01,
                             self.generate_x,
                             self.generate_y,
                             [None, True, None, False],
                             [2 * np.pi])

    def generate_x(self,
                   periods: float = None,
                   linspace: bool = True,
                   x_offset: float = None,
                   start_at_0: bool = False):
        if periods is None:
            periods = 1
        if x_offset is None:
            x_offset = self.offsets[0]

        if linspace:
            x = np.linspace((0 if start_at_0 else 1) * (-x_offset - (self.period * periods)),
                            x_offset + (self.period * periods), self.resolution)
        else:
            x = np.arange((0 if start_at_0 else 1) * (-x_offset - (self.period * periods)),
                          x_offset + (self.period * periods), (self.period / self.resolution))

        return x

    def generate_y(self, x, period_constant=(2 * np.pi)):
        dampened = dampen(self.decay_constant,
                          self.func((period_constant * (x + self.offsets[0]) / self.period)))
        y = (self.amplitude * dampened) + self.offsets[1]
        return y

    def plot(self,
             periods: float = 1,
             line_width: float = 1):
        x = self.generate_x(periods=periods)
        y = self.generate_y(x)

        plot_2D(x, y, line_width)

    def animate(self,
                speed: float = 1,
                line_width: float = 1):
        self.anim.animate(speed, line_width)

    def __add__(self, other):
        if _check_type(other):
            new_func = lambda x: self.func(x + self.offsets[0]) + other.func(x + other.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            new_func = lambda x: self.func(x + self.offsets[0]) + self.offsets[1] + other
            return Wave(func=new_func,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot add types {0} and {1}".format(type(self), type(other)))

    def __radd__(self, other):
        if _check_type(other):
            new_func = lambda x: self.func(x + self.offsets[0]) + other.func(x + other.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            new_func = lambda x: self.func(x + self.offsets[0]) + self.offsets[1] + other
            return Wave(func=new_func,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot add types {0} and {1}".format(type(self), type(other)))

    def __sub__(self, other):
        if _check_type(other):
            new_func = lambda x: self.func(x + self.offsets[0]) - other.func(x + other.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            new_func = lambda x: self.func(x + self.offsets[0]) + self.offsets[1] - other
            return Wave(func=new_func,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot subtract types {0} and {1}".format(type(self), type(other)))

    def __rsub__(self, other):
        if _check_type(other):
            new_func = lambda x: other.func(x + other.offsets[0]) - self.func(x + self.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            new_func = lambda x: other - (self.func(x + self.offsets[0]) + self.offsets[1])
            return Wave(func=new_func,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot subtract types {0} and {1}".format(type(self), type(other)))

    def __mul__(self, other):
        if _check_type(other):
            warnings.warn("The period of this function is ambiguous, and the generated period may be "
                          "incorrect. \nHowever, this attribute can be manually edited with <WaveObj>"
                          ".period = <new_period>", RuntimeWarning)
            new_func = lambda x: self.func(x + self.offsets[0]) * other.func(x + other.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            return Wave(func=self.func,
                        amplitude=self.amplitude * other,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot multiply types {0} and {1}".format(type(self), type(other)))

    def __rmul__(self, other):
        if _check_type(other):
            warnings.warn("The period of this function is ambiguous, and the generated period may be "
                          "incorrect. \nHowever, this attribute can be manually edited with <WaveObj>"
                          ".period = <new_period>", RuntimeWarning)
            new_func = lambda x: self.func(x + self.offsets[0]) * other.func(x + other.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            return Wave(func=self.func,
                        amplitude=self.amplitude * other,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot multiply types {0} and {1}".format(type(self), type(other)))

    def __truediv__(self, other):
        if _check_type(other):
            warnings.warn("The period of this function is ambiguous, and the generated period may be "
                          "incorrect. \nHowever, this attribute can be manually edited with <WaveObj>"
                          ".period = <new_period>", RuntimeWarning)
            new_func = lambda x: self.func(x + self.offsets[0]) / other.func(x + other.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            return Wave(func=self.func,
                        amplitude=self.amplitude / other,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot divide types {0} and {1}".format(type(self), type(other)))

    def __rtruediv__(self, other):
        if _check_type(other):
            warnings.warn("The period of this function is ambiguous, and the generated period may be "
                          "incorrect. \nHowever, this attribute can be manually edited with <WaveObj>"
                          ".period = <new_period>", RuntimeWarning)
            new_func = lambda x: other.func(x + other.offsets[0]) / self.func(x + self.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            return Wave(func=self.func,
                        amplitude=self.amplitude / other,
                        period=self.period,
                        offsets=(0, 0),
                        resolution=self.resolution)
        raise TypeError("Cannot divide types {0} and {1}".format(type(self), type(other)))

    def __call__(self, other):
        if _check_type(other):
            warnings.warn("The period of this function is ambiguous, and the generated period may be "
                          "incorrect. \nHowever, this attribute can be manually edited with <WaveObj>"
                          ".period = <new_period>", RuntimeWarning)
            new_func = lambda x: self.func(other.func(x + other.offsets[0]) + self.offsets[0]) + \
                                 self.offsets[1] + other.offsets[1]
            return Wave(func=new_func,
                        period=__lcm__(self.period, other.period),
                        offsets=(0, 0),
                        resolution=int((self.resolution + other.resolution) / 2))
        if isinstance(other, (int, float, complex)) and not isinstance(other, bool):
            return np.around(self.func(other), decimals=10)
        raise TypeError("Cannot call type {0} on type {1}".format(type(self), type(other)))
