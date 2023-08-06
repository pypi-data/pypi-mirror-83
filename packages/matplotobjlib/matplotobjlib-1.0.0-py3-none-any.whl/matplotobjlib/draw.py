"""
Provides facilities for graphing in matplotlib. See draw_graph for the main drawing function
"""
import dataclasses
import tkinter as tk
from tkinter import ttk
from typing import Optional, Sequence, Union

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

from matplotobjlib.subplot import SubPlot


@dataclasses.dataclass
class SubplotsAdjust:
    left: Optional[float] = None
    bottom: Optional[float] = None
    right: Optional[float] = None
    top: Optional[float] = None
    wspace: Optional[float] = None
    hspace: Optional[float] = None


@dataclasses.dataclass
class FigureOptions:
    subplots: Sequence[Sequence[SubPlot]]
    title: Optional[str] = None
    adjust: SubplotsAdjust = SubplotsAdjust(hspace=0.6, wspace=0.3)


class TkFigure(ttk.Frame):
    DEFAULT_FONT_SIZE = 23
    DEFAULT_TITLE_SIZE = 25

    def __init__(
        self,
        parent: tk.Widget,
        options: FigureOptions,
    ):
        ttk.Frame.__init__(self, parent)
        self._fig = Figure()
        self._subplots = []
        self._canvas = FigureCanvas(self._fig, self)
        self._canvas.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)
        toolbar = NavigationToolbar2Tk(self._canvas, self)
        toolbar.update()

        num_rows = len(options.subplots)
        num_columns = max(len(graphs) for graphs in options.subplots)
        for i in range(num_rows):
            for j in range(num_columns):
                subplot = options.subplots[i][j]
                if subplot is not None:
                    index = (i * num_columns) + j + 1
                    ax = self._fig.add_subplot(num_rows, num_columns, index)
                    subplot.set_axis(ax)
                    self._subplots.append(subplot)
        self._fig.suptitle(options.title or "", fontweight="bold", fontsize=self.DEFAULT_TITLE_SIZE)
        self._fig.subplots_adjust(**dataclasses.asdict(options.adjust))

        self.draw()

    def draw(self) -> None:
        for subplot in self._subplots:
            subplot.draw()

    def update_plot(self) -> None:
        self._canvas.draw()
        self._canvas.flush_events()


def draw(options: FigureOptions) -> None:
    """
    Draws subplots on a new Tk root window and runs mainloop until it's closed

    Args:
        subplots: A 2d sequence of SubPlot objects. It's a list of columns and each column contains the SubPlot's that
            need to be drawn
        title: The title for the tk window and for the plot
    """
    if isinstance(subplots, SubPlot):
        subplots = [[subplots]]
    root = tk.Tk()
    root.title("Plot" if options.title is None else options.title)
    root.geometry("1050x700")
    figure = TkFigure(root, options)
    figure.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
