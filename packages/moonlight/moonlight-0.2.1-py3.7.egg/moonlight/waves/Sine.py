import numpy as np
from .Wave import Wave
from ..utils import dampen, plot_2D


class Sine(Wave):
    def __init__(self,
                 amplitude: float = 1,
                 period: float = (2 * np.pi),
                 offsets: tuple = (0, 0),
                 decay_constant: float = 0,
                 resolution: int = 500):
        super().__init__(np.sin, amplitude, period, offsets, decay_constant, resolution)
        self.anim.x_args[3] = True
