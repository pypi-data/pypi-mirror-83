from functions import configure
from tkinter import *
from tkinter import ttk
from frames.etf_list import EtfList
from frames.add_etf import AddEtf
from frames.sell_etf import SellEtf


class RightFrame(ttk.Frame):
    """Class representing the right frame of the GUI"""

    def __init__(self, root, app):
        """
        Initialize the class given a root Frame and the App Frame.
        :param root: ttk.Frame 
        :param app: ttk.Frame
        :return None 
        """
        super().__init__(root)
        self.root = root
        self.app = app
        self.p = self.app.p
        self.etf_list = EtfList(self)
        self.etf_list.grid(row=0, column=0)
        ttk.Separator(self, orient=HORIZONTAL).grid(row=1, column=0, sticky='nswe', padx=(0,20))
        self.add_etf = AddEtf(self)
        self.add_etf.grid(row=2, column=0)
        ttk.Separator(self, orient=HORIZONTAL).grid(row=3, column=0, sticky='nswe', padx=(0,20))
        self.sell_etf = SellEtf(self)
        self.sell_etf.grid(row=4, column=0)
        configure(self, 5, 1)
