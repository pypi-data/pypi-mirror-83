import dataclasses
import enum
from typing import Iterable, Optional, Tuple, Union

import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes._axes import Axes

from matplotobjlib.plotable import Plotable
from matplotobjlib.type_hints import Value


class LogType(enum.Enum):
    Neither = enum.auto()
    X = enum.auto()
    Y = enum.auto()
    Both = enum.auto()


class Axis(enum.Enum):
    X = "x"
    Y = "y"


@dataclasses.dataclass
class TickOptions:
    labels: Optional[Iterable[str]] = None
    use_offset: Optional[bool] = None
    values: Optional[Iterable[Value]] = None
    size: Optional[int] = None
    style: Optional[str] = None

    def apply(self, axes: Axes, *, axis: Axis) -> None:
        if self.labels is not None:
            (axes.set_xticklabels if axis == axis.X else axes.set_yticklabels)(self.labels)
        if self.values is not None:
            (axes.set_xticks if axis == axis.X else axes.set_yticks)(self.values)
        format_kwargs = {}
        if self.style is not None:
            format_kwargs["style"] = self.style
        if self.use_offset is not None:
            format_kwargs["useOffset"] = self.use_offset
        if format_kwargs:
            axes.ticklabel_format(axis=axis.value, **format_kwargs)
        if self.size is not None:
            ax = axes.xaxis if axis == Axis.X else axes.yaxis
            for tick in ax.get_major_ticks():
                tick.label.set_fontsize(self.size)


class SubPlot:
    """
    Creates a holder class that stores the info to make a single matplotlib subplot. Many GraphSettings could be added
    and various configurations can be changed

    Attributes:
        graphs: A list of GraphSettings that should be plotted
        x_label: The label for the x-axis of this subplot
        y_label: The label for the y-axis of this subplot
        title: The title for this subplot
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        *plotables: Plotable,
        x_label: str = "",
        y_label: str = "",
        title: str = "",
        log: Optional[LogType] = None,
        axis_label_size: int = 23,
        title_font_size: int = 23,
        legend_size: Optional[int] = None,
        x_range: Optional[Tuple[Optional[Value], Optional[Value]]] = None,
        y_range: Optional[Tuple[Optional[Value], Optional[Value]]] = None,
        x_tick_options: TickOptions = TickOptions(use_offset=True),
        y_tick_options: TickOptions = TickOptions(style="sci", use_offset=False),
    ):
        """
        Creates a new SubPlot object

        Args:
            args: A list of GraphSettings may be provided or they may be provided separately and collected
            x_label: The label for the x-axis of this subplot
            y_label: The label for the y-axis of this subplot
            title: The title for this subplot
        """
        self.plotables = list(plotables)
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.x_log = log in (LogType.X, LogType.Both)
        self.y_log = log in (LogType.Y, LogType.Both)
        self.axis_label_size = axis_label_size
        self.title_size = title_font_size
        self.legend_size = legend_size
        self.x_range = x_range
        self.y_range = y_range
        self._axis = None
        self._x_tick_options = x_tick_options
        self._y_tick_options = y_tick_options

    def set_axis(self, ax: Axes) -> None:
        self._axis = ax
        ax.set_ylabel(self.y_label, fontsize=self.axis_label_size)
        ax.set_xlabel(self.x_label, fontsize=self.axis_label_size)
        ax.set_title(self.title, fontsize=self.title_size, fontweight="bold")
        self._x_tick_options.apply(ax, axis=Axis.X)
        self._y_tick_options.apply(ax, axis=Axis.Y)
        if self.x_log:
            ax.set_xscale("log", basey=np.e)
            ax.grid(which="major")
        if self.y_log:
            ax.set_yscale("log", basey=np.e)
            ax.grid(which="minor")
        if self.x_range is not None:
            ax.set_xlim(*self.x_range)
        if self.y_range is not None:
            ax.set_ylim(*self.y_range)

    def draw(self) -> None:
        has_labels = False
        for plotable in self.plotables:
            artist = plotable.draw(self._axis, self.x_log, self.y_log)
            if not artist.get_label().startswith("_"):
                has_labels = True

        if has_labels:
            self._axis.legend(loc="best", fontsize=self.legend_size)

    def add_plotable(self, plotable: Plotable) -> Optional[Artist]:
        self.plotables.append(plotable)
        if self._axis:
            handle = plotable.draw(self._axis, self.x_log, self.y_log)
            self._axis.legend()
            return handle
