from tkinter import *
from tkinter import ttk
from functions import *


class EtfList(ttk.Frame):
    """Class representing the frame conteining the ETF list"""

    def __init__(self, root):
        """
        Initialize the class given a root Frame and the portfolio object.
        :param root: ttk.Frame
        :param portfolio: Portfolio
        :return None
        """
        super().__init__(root)
        self.p = root.p
        self.app = root.app
        self.c_frame = self.app.central_frame
        self.names = tuple([x for x in self.p.etfs.keys()])
        self.etf_names = StringVar(value=self.names)
        self.lbox = Listbox(self, listvariable=self.etf_names, height=6)
        self.lbox.grid(row=0, column=0)
        self.lbox.bind('<<ListboxSelect>>', lambda e: self.etf_graph(self.names[self.lbox.curselection()[0]]))
        self.scroll = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbox.yview)
        self.lbox.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1)
        configure(self, 2, 1)
    
    def etf_graph(self, etf):
        """
        Draws the quity graph about the given ETF.
        :param etf: ETF
        :return None
        """
        self.app.left_frame.clear_radio()
        self.c_frame = self.app.new_central_frame()
        fig, ax = self.p.get_etf_by_name(etf).equity_line()
        graph(fig, self.c_frame)
    
    def clear_box(self):
        """
        Clears the box from the selection.
        :return None
        """
        self.lbox.select_clear(0,len(self.names)-1)
    
    def refresh(self):
        """
        Refresh the ETFs list adding the new one.
        :return None
        """
        self.names = tuple([x for x in self.p.etfs.keys()])
        self.etf_names = StringVar(value=self.names)
        self.lbox = Listbox(self, listvariable=self.etf_names, height=6)
        self.lbox.grid(row=0, column=0)
        self.lbox.bind('<<ListboxSelect>>', lambda e: self.etf_graph(self.names[self.lbox.curselection()[0]]))
        self.scroll = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbox.yview)
        self.lbox.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1)