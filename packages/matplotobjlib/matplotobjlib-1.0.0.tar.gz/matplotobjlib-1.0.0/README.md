# matplotobjlib

This module is a wrapper for matplotlib, that enables creating plots in an easier declarative, more object-oriented
format.

All functions and types are importable directly from `matplotobjlib`. The easiest way to get started is with `matplotoblib.draw(...)`. This function takes either a single `Suplot` object or a 2d sequence of `Subplot`s where each inner sequence represents a row. Each `Subplot` consists of 1 or more `Plotable`s, the most useful being `Graph`.

    # examples/sin.py

    from matplotobjlib import draw, Graph, SubPlot
    import numpy as np

    xs = np.arange(-2*np.pi, 2*np.pi, 0.01)
    ys = np.sin(xs)
    draw(SubPlot(Graph(xs, ys, plot_type="-"), x_label="x", y_label="sin(x)"), title="sin")

<img src="https://raw.githubusercontent.com/larashores/matplotobjlib/master/images/sin.png" title=examples/sin.py width="600">

    # examples/trig.py

    from matplotobjlib import draw, Graph, SubPlot
    import numpy as np

    xs = np.arange(-2*np.pi, 2*np.pi, 0.01)
    draw(
        [
            [
                SubPlot(Graph(xs, np.sin(xs), plot_type="-"), x_label="x", y_label="sin(x)"),
                SubPlot(Graph(xs, np.cos(xs), plot_type="-"), x_label="x", y_label="cos(x)"),
            ],
            [
                SubPlot(Graph(xs, np.tan(xs), plot_type="-"), x_label="x", y_label="tan(x)"),
                SubPlot(Graph(xs, np.arcsin(xs), plot_type="-"), x_label="x", y_label="sin$^{-1}$(x)"),
            ]
        ],
        title="Trigonometry",
    )

<img src="https://raw.githubusercontent.com/larashores/matplotobjlib/master/images/trig.png" title=examples/trig.py width="600">

Additionally, for more control over the window, it can be accessed as a tkinter widget through `TkFigure`. The `draw(...)` function even uses this internally.

    # examples/widget.py

    import tkinter as tk
    import numpy as np
    from matplotobjlib import Graph, SubPlot, TkFigure

    ts = np.arange(0, 10, 0.01)
    xs = [t * np.cos(t) for t in ts]
    ys = [t * np.sin(t) for t in ts]

    root = tk.Tk()
    widget = TkFigure(
        root, [[SubPlot(Graph(xs, ys, plot_type="-"), x_label="t*cos(t)", y_label="t*sin(t)")]], title="examples/widget.py"
    )
    widget.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


<img src="https://raw.githubusercontent.com/larashores/matplotobjlib/master/images/widget.png" title=examples/widget.py width="600">