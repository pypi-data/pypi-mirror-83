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
        self.lbox = Listbox(self, listvariable=self.etf_names, height=6, justify='center')
        self.lbox.grid(row=0, column=0)
        self.lbox.bind('<<ListboxSelect>>', lambda e: self.list_box_selected())
        self.scroll = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbox.yview)
        self.lbox.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1)
        configure(self, 2, 1)
    
    def etf_graph(self, etf, **kwargs):
        """
        Draws the quity graph about the given ETF.
        :param etf: ETF
        :return None
        """
        clear_selection('EtfGraphs', self)
        fig, ax = self.p.get_etf_by_name(etf).equity_line(**kwargs)
        if 'pct' in kwargs:
            pct = BooleanVar(value=kwargs['pct'])
        else:
            pct = BooleanVar(value=True)
        if 'sp500' in kwargs:
            sp500 = BooleanVar(value=kwargs['sp500'])
        else:
            sp500 = BooleanVar()
        frame = ttk.Frame(self.c_frame)
        frame.pack(side=BOTTOM)
        ttk.Checkbutton(frame, text='Percentuale', variable=pct, onvalue=True, offvalue=False, command=lambda: self.etf_graph(etf, pct=pct.get(), sp500=sp500.get())).grid(row=0, column=0, pady=20, padx=20)
        ttk.Checkbutton(frame, text='S&P500', variable=sp500, onvalue=True, offvalue=False, command=lambda: self.etf_graph(etf, pct=pct.get(), sp500=sp500.get())).grid(row=0, column=2, pady=20, padx=20)
        configure(frame, 0, 3)
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
        self.lbox = Listbox(self, listvariable=self.etf_names, height=6, justify='center')
        self.lbox.grid(row=0, column=0)
        self.lbox.bind('<<ListboxSelect>>', lambda e: self.list_box_selected())
        self.scroll = ttk.Scrollbar(self, orient=VERTICAL, command=self.lbox.yview)
        self.lbox.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1)
    
    def list_box_selected(self):
        """
        Functions that gets triggered when a <<LiistboxSelected>> event occurs. It draws the graph belonging
        to the selected etf if there is a present selction, meaning the event wasn't referring to another ListBox. 
        :return None
        """
        selections = self.lbox.curselection()
        if len(selections) > 0:
            etf_name = self.names[selections[0]]
            self.etf_graph(etf_name)
