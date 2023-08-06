from tkinter import * 
from tkinter import ttk
from etf import ETF
from functions import * 


class AddEtf(ttk.Frame):
    """Class representing a Frame responsable for the adding of an ETF"""

    def __init__(self, root):
        """
        Given the master instaciate a class handling the adding function
        :param root: ttk.Frame
        """
        super().__init__(root)
        self.p = root.p
        self.root = root
        ttk.Label(self, text='AGGIUNGI ETF').grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self, text='Ticker', anchor='w', justify='left').grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self, text='Data Acquisto', anchor='w', justify='left').grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(self, text='Numero di Azioni', anchor='w', justify='left').grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(self, text="Prezzo d'Acquisto", anchor='w', justify='left').grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(self, text='Commissioni', anchor='w', justify='left').grid(row=5, column=0, padx=5, pady=5)
        self.tickerVar = StringVar()
        self.dateVar = StringVar(value='Es. 10-12-2020')
        self.nVar = IntVar()
        self.priceVar = DoubleVar()
        self.commVar = DoubleVar()
        ttk.Entry(self, textvariable=self.tickerVar, width=12).grid(row=1, column=1)    
        self.e = ttk.Entry(self, textvariable=self.dateVar, width=12)
        self.e.grid(row=2, column=1)   
        ttk.Entry(self, textvariable=self.nVar, width=12).grid(row=3, column=1)           
        ttk.Entry(self, textvariable=self.priceVar, width=12).grid(row=4, column=1)           
        ttk.Entry(self, textvariable=self.commVar, width=12).grid(row=5, column=1) 
        self.result = ttk.Label(self, text='')
        self.result.grid(row=6, column=1) 
        self.button = ttk.Button(self, text='Aggiungi', command=self.add_etf)
        self.button.grid(row=6, column=0, pady=10)

    def add_etf(self):
        """
        When the Add button is clicked try adding the ETF. Display the result on the adjacent label.
        :return None
        """
        try:
            self.p.add_etf(ETF(self.tickerVar.get(), date_from_text(self.e.get()), self.nVar.get(), self.priceVar.get(), self.commVar.get(), info=self.p.infoFile.split('Info.csv')[0]+'ETFs/'))     
            self.tickerVar.set('')
            self.dateVar.set('')
            self.nVar.set('')
            self.priceVar.set('')
            self.commVar.set('')
            self.result.configure(text='ETF aggiunto !')
            self.root.etf_list.refresh()
        except:
            self.result.configure(text='Errore !')   