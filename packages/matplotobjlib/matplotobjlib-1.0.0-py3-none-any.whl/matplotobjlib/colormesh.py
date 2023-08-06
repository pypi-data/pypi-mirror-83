from typing import Optional

import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes._axes import Axes
from matplotlib.colors import Colormap

from matplotobjlib.plotable import Plotable
from matplotobjlib.type_hints import Range, Value


class Colormesh(Plotable):
    def __init__(self, values: np.ndarray, colormap: Optional[Colormap] = None):
        self._values = values
        self._colormap = colormap

    def draw(self, axes: Axes, x_log: bool, y_log: bool) -> Artist:
        return axes.pcolormesh(self._values, cmap=self._colormap)
