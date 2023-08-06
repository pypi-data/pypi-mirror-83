from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *


def graph(fig, frame):
    """
    Draws a graph on the screen given the frame to draew it on and the figure object.
    :param fig: matplotlib.pyplot.Figure
    :param frame: ttk.Frame
    :return None
    """
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    
def configure(frame, rows, columns):
    """
    Configure the frame given the number of rows and columns it is divided in.
    :param frame: ttk.Frame
    :param rows: int
    :param columns: int
    :return None
    """
    for row in range(rows):
        frame.rowconfigure(row, weight=1)
    for col in range(columns):
        frame.columnconfigure(col, weight=1)