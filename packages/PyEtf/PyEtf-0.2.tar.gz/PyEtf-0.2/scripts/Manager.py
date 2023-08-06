#!python

from tkinter import *
from tkinter import ttk
from portfolio import Portfolio
from right_frame import RightFrame
from left_frame import LeftFrame
from functions import *


class App:

    def __init__(self, root):
        self.p = Portfolio()
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        for y in range(7):
            self.mainframe.columnconfigure(y, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.central_frame = ttk.Frame(self.mainframe)
        self.central_frame.grid(row=0, column=1, columnspan=5, sticky=(E, W, N, S), padx=15)

        self.left_frame = LeftFrame(self.mainframe, self)
        self.left_frame.grid(row=0, column=0, sticky=(W, N, S, E), padx=15)

        self.right_frame = RightFrame(self.mainframe, self)
        self.right_frame.grid(row=0, column=6, sticky=(E, N, S, W), padx=15)
        
        self.left_frame.last_day()

    def stats(self):
        self.new_central_frame()
        self.clear_radio()
        self.right_frame.etf_list.clear_box()
    
    def new_central_frame(self):
        """
        Creates a new central frame in order to be able to show new things on it.
        :reeturn ttk.Frame
        """
        self.central_frame.destroy()
        self.central_frame = ttk.Frame(self.mainframe)
        self.central_frame.grid(row=0, column=1, columnspan=5, sticky=(E, W, N, S), padx=15)
        return self.central_frame


def main():
    root = Tk()
    root.title('Portfolio Manager by Dodo')
    root.geometry("1400x700")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
