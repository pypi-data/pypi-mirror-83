from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
from datetime import date, timedelta


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
    # toolbar = NavigationToolbar2Tk(canvas, frame)
    # toolbar.config(background='#ececec')
    # toolbar._message_label.config(background='#ececec')
    # toolbar.update()
    # canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
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
    for column in range(columns):
        frame.columnconfigure(column, weight=1)

def date_from_text(string):
    """
    Convert a string text in the 'day-month-year' format into a datetime.date object.
    :param string: str
    :return datetime.date
    """
    day, month, year = list(map(int, string.split('-')))
    return date(year, month, day)

def clear_selection(inputWidget, inputFrame):
    """
    Clears the button selection leaving selected only the button from the inputFrame parameter.
    Possible inputWidget parameters: 'PortfolioGraphs' - 'Button' - 'Tables' - 'EtfGraphs'.
    :param inputWidget: str 
    :param inputFrame: ttk.Frame
    :return None
    """
    if inputWidget == 'PortfolioGraphs' or inputWidget == 'Tables':
        inputFrame.app.right_frame.etf_list.clear_box()
    elif inputWidget == 'Button':
        inputFrame.clear_radio()
        inputFrame.app.right_frame.etf_list.clear_box()
    elif inputWidget == 'EtfGraphs':
        inputFrame.app.left_frame.clear_radio()
    inputFrame.c_frame = inputFrame.app.new_central_frame()

def nextWeekDay(day):
    """
    Calculates the next week day from the date givena as a parameter.
    :param day: datetime.date 
    :return datetime.date
    """
    weekDay = day.weekday()
    if weekDay < 4 or weekDay == 6:
        return day + timedelta(1)
    else:
        return day + timedelta(7-weekDay)
