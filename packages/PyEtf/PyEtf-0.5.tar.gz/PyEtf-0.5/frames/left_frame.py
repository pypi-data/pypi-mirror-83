from tkinter import *
from tkinter import ttk
from tkinter import font

from matplotlib.pyplot import text
from functions import *
from datetime import date


class LeftFrame(ttk.Frame):
    """Class representing the left frame of the GUI"""

    BAR_TABLE = {'Mensile': 'M', 'Settimanale': 'W', 'Annuale': 'Y'}
    BAR_TABLE_R = {'M': 'Mensile', 'W': 'Settimanale', 'Y': 'Annuale'}

    def __init__(self, root, app):
        """
        Initialize the class given a root Frame and the App Frame.
        :param root: ttk.Frame 
        :param app: ttk.Frame
        :return None 
        """
        super().__init__(root)
        self.app = app
        self.c_frame = self.app.central_frame
        self.p = self.app.p
        ttk.Button(self, text='Dati Ultimo Giorno', command=self.last_day).grid(row=0, column=0, pady=(20,0))
        self.graph = StringVar()
        ttk.Radiobutton(self, text='Grafico Valore', command=self.value_line, variable=self.graph, value='value').grid(row=2, column=0)
        ttk.Radiobutton(self, text='Grafico Equity', command=self.equity_graph, variable=self.graph, value='equity').grid(row=3, column=0)
        ttk.Radiobutton(self, text='Grafico Investimento', command=self.investment_line, variable=self.graph, value='invested').grid(row=4, column=0)
        ttk.Radiobutton(self, text='Grafico a Barre', command=self.bar_chart, variable=self.graph, value='bar').grid(row=5, column=0)
        ttk.Radiobutton(self, text='Grafico a Torta', command=self.pie_chart, variable=self.graph, value='pie').grid(row=6, column=0)
        ttk.Separator(self, orient=HORIZONTAL).grid(row=7, column=0, sticky='nswe', padx=(20, 0))
        ttk.Radiobutton(self, text='Tabella Investimenti', command=self.draw_table, variable=self.graph, value='inv_table').grid(row=8, column=0)
        ttk.Radiobutton(self, text='Tabella Portafoglio', command=self.draw_table, variable=self.graph, value='port_table').grid(row=9, column=0)
        ttk.Button(self, text='Statistiche', command=self.show_stats).grid(row=11, column=0)
        ttk.Button(self, text='Chiudi', command=root.quit).grid(row=13, column=0, pady=(0,20))
        configure(self, 14, 1)
    
    def value_line(self):
        """
        Draws the value graph on the central frame.
        :return None
        """
        clear_selection('PortfolioGraphs', self)
        fig, ax = self.p.value_line()
        graph(fig, self.c_frame)
    
    def investment_line(self):
        """
        Draws the value graph on the central frame.
        :return None
        """
        clear_selection('PortfolioGraphs', self)
        fig, ax = self.p.investment_line()
        graph(fig, self.c_frame)

    def equity_graph(self, **kwargs):
        """
        Draws the equity graph on the central frame based on the arguments passed as parameters.
        :param kwargs: dict
        :return None
        """
        clear_selection('PortfolioGraphs', self)
        fig, ax = self.p.equity_line(**kwargs)
        if 'pct' in kwargs:
            pct = BooleanVar(value=kwargs['pct'])
        else:
            pct = BooleanVar()
        if 'sp500' in kwargs:
            sp500 = BooleanVar(value=kwargs['sp500'])
        else:
            sp500 = BooleanVar()
        frame = ttk.Frame(self.c_frame)
        frame.pack(side=BOTTOM)
        ttk.Checkbutton(frame, text='Percentuale', variable=pct, onvalue=True, offvalue=False, command=lambda: self.equity_graph(pct=pct.get(), sp500=sp500.get())).grid(row=0, column=0, pady=20, padx=20)
        ttk.Checkbutton(frame, text='S&P500', variable=sp500, onvalue=True, offvalue=False, command=lambda: self.equity_graph(pct=pct.get(), sp500=sp500.get())).grid(row=0, column=2, pady=20, padx=20)
        configure(frame, 0, 3)
        graph(fig, self.c_frame)
    
    def bar_chart(self, **kwargs):
        """
        Draws the bar chart on the central frame based on the arguments passed as parameters.
        :param kwargs: dict
        :return None
        """
        clear_selection('PortfolioGraphs', self)
        fig, ax = self.p.bar_chart(**kwargs)
        if 'period' in kwargs:
            tf = StringVar(value=self.BAR_TABLE_R[kwargs['period']])
        else:
            tf = StringVar(value='Mensile')
        if 'annot' in kwargs:
            annot = BooleanVar(value=kwargs['annot'])
        else:
            annot = BooleanVar(value=True)
        frame = ttk.Frame(self.c_frame)
        frame.pack(side=BOTTOM)
        self.combo = ttk.Combobox(frame, textvariable=tf, values=('Settimanale','Mensile','Annuale'), state='readonly')
        self.combo.grid(row=0, column=0, pady=20, padx=20)
        self.combo.bind('<<ComboboxSelected>>', lambda e: self.select_time_frame(tf, annot))
        ttk.Checkbutton(frame, text='Annotazioni', variable=annot, onvalue=True, offvalue=False, command=lambda: self.bar_chart(period=self.BAR_TABLE[tf.get()], annot=annot.get())).grid(row=0, column=2, pady=20, padx=20)
        configure(frame, 0, 3)
        graph(fig, self.c_frame)
    
    def pie_chart(self, **kwargs):
        """
        Draws the pie chart on the central frame based on the arguments passed as parameters.
        :param kwargs: dict
        :return None
        """
        clear_selection('PortfolioGraphs', self)
        fig, ax = self.p.pie_chart(**kwargs)
        if 'pct' in kwargs:
            pct = BooleanVar(value=kwargs['pct'])
        else:
            pct = BooleanVar(value=True)
        if 'day' in kwargs:
            day = StringVar(value=kwargs['day'].strftime('%d-%m-%Y'))
        else:
            day = StringVar(value=date.today().strftime('%d-%m-%Y'))
        frame = ttk.Frame(self.c_frame)
        frame.pack(side=BOTTOM)
        ttk.Label(frame, text='Data', anchor='w', justify='left').grid(row=0, column=0, rowspan=2, padx=20)
        ttk.Entry(frame, textvariable=day, width=10, justify='center').grid(row=0, column=1, pady=(12, 3))
        ttk.Button(frame, text='Aggiorna', command=lambda : self.pie_chart(pct=pct.get(), day=date_from_text(day.get()))).grid(row=1, column=1, pady=(3,12))
        ttk.Checkbutton(frame, text='Percentuale', variable=pct, onvalue=True, offvalue=False, command=lambda: self.pie_chart(pct=pct.get(), day=date_from_text(day.get()))).grid(row=0, column=3, rowspan=2, pady=20, padx=20)
        configure(frame, 2, 3)
        graph(fig, self.c_frame)
    
    def select_time_frame(self, time_frame, annotations):
        """
        Calls the bar chart function setting the proper parameters based on the time frame and annotations choice.
        :param time_frame: tkinter.StringVar
        :param annotations: tkinter.BooleanVar
        :return None
        """
        self.combo.selection_clear()
        self.bar_chart(period=self.BAR_TABLE[time_frame.get()], annot=annotations.get())
    
    def last_day(self):
        """
        Shows data (P/L and P/L %) about the last trading day.
        :return None
        """
        clear_selection('Button', self)
        if len(self.p.etfs) > 0:
            table = self.p.last_day_table()
            ttk.Label(self.c_frame, text="DATI RELATIVI ALL'ULTIMA GIORNATA", style='Title.TLabel').grid(row=0, column=0, columnspan=3, pady=(10,0))
            ttk.Label(self.c_frame, text=self.p.data.index[-1].strftime('%A %d %B %Y'), style='Date.TLabel').grid(row=1, column=0, columnspan=3)
            ttk.Label(self.c_frame, text='Ticker', style='Head.TLabel').grid(row=2, column=0)
            ttk.Label(self.c_frame, text='Profit/Loss (€)', style='Head.TLabel').grid(row=2, column=1)
            ttk.Label(self.c_frame, text='Profit/Loss (%)', style='Head.TLabel').grid(row=2, column=2)
            for i, etf in enumerate(table.index):
                gains = table.loc[etf, "P/L"]
                if i == len(table.index) - 1:
                    styleHead = 'Head.TLabel'
                    ttk.Label(self.c_frame, text=etf, style=styleHead).grid(row=i+3, column=0)
                    if gains > 0:
                        styleNumbers = 'PositiveBold.TLabel'
                    else:
                        styleNumbers = 'NegativeBold.TLabel'
                else:
                    if gains > 0:
                        styleNumbers = 'Positive.TLabel'
                    else:
                        styleNumbers = 'Negative.TLabel'
                    ttk.Label(self.c_frame, text=etf).grid(row=i+3, column=0)
                ttk.Label(self.c_frame, text=f'{round(gains,2)} €', style=styleNumbers).grid(row=i+3, column=1)
                ttk.Label(self.c_frame, text=f'{round(table.loc[etf, "P/L%"],2)} %', style=styleNumbers).grid(row=i+3, column=2)
            configure(self.c_frame, len(table.index)+4, 3)
        else:
            ttk.Label(self.c_frame, text='INSERISCI UN ETF PRIMA DI CLICCARE QUALSIASI COSA\n ALTRIMENTI IMPAZZISCE TUTTO!!').grid(row=0,column=0) 
            configure(self.c_frame, 1, 1)
    
    def draw_table(self):
        """
        Shows data about investments or portfolio depending on the radiobutton cliccked.
        :return None
        """
        clear_selection('Tables', self)
        var = self.graph.get()
        if var == 'inv_table':
            table = self.p.investments_table()
            ttk.Label(self.c_frame, text="DATI RELATIVI AGLI INVESTIMENTI", style='Title.TLabel').grid(row=0, column=0, columnspan=len(table.columns), pady=(10,0))
            table.insert(1, 'Buying Date', table.index) 
        else:
            table = self.p.portfolio_table()
            ttk.Label(self.c_frame, text="DATI RELATIVI AL PORTAFOGLIO", style='Title.TLabel').grid(row=0, column=0, columnspan=len(table.columns))
            table.insert(0, 'Ticker', table.index) 
        table['Idx'] = [x for x in range(len(table))]
        table.set_index('Idx', inplace=True)  
        for i, col in enumerate(table.columns):
            ttk.Label(self.c_frame, text=col, style='Head.TLabel').grid(row=1, column=i)
        for y in table.index:
            for x, col in enumerate(table.columns):
                ttk.Label(self.c_frame, text=table.loc[y, col]).grid(row=y+2, column=x)
        configure(self.c_frame, len(table.index)+2, len(table.columns))
    
    def show_stats(self, day='today'):
        """
        Shows statistitcs about portfolio given the given date. 
        :return None
        """
        clear_selection('Button', self)
        if day == 'today':
            day = self.p.data.index[-1]
            dayVar = StringVar(value=date.today().strftime('%d-%m-%Y'))
        else:
            day = self.p._first_good_date(day)
            dayVar = StringVar(value=day.strftime('%d-%m-%Y'))
        ttk.Label(self.c_frame, text="STATISTICHE PORTAFOGLIO", style='Title.TLabel').grid(row=0, column=0, columnspan=2)
        ttk.Label(self.c_frame, text="Quantità investita:").grid(row=1, column=0)
        ttk.Label(self.c_frame, text=f'{self.p.invested_amount(day)} €').grid(row=1, column=1)
        ttk.Label(self.c_frame, text="Valore del portafoglio:").grid(row=2, column=0)
        ttk.Label(self.c_frame, text=f'{self.p.value(day)} €').grid(row=2, column=1)
        ttk.Label(self.c_frame, text="Profitto / Perdita (€):").grid(row=3, column=0)
        ttk.Label(self.c_frame, text=f'{self.p.profit_loss(day)} €').grid(row=3, column=1)
        ttk.Label(self.c_frame, text="Profitto / Perdita (%):").grid(row=4, column=0)
        ttk.Label(self.c_frame, text=f'{self.p.profit_loss(day, True)} %').grid(row=4, column=1)
        ttk.Label(self.c_frame, text="Profitto / Perdita annualizzato (%):").grid(row=5, column=0)
        ttk.Label(self.c_frame, text=f'{self.p.annualized_gains(day)} %').grid(row=5, column=1)
        ttk.Label(self.c_frame, text="Data:").grid(row=6, column=0, padx=(70,0), pady=(30,0))
        ttk.Entry(self.c_frame, textvariable=dayVar, width=12, justify='center').grid(row=6, column=1, padx=(0,70), pady=(30,0))
        ttk.Button(self.c_frame, text='Aggiorna', command=lambda: self.show_stats(day=date_from_text(dayVar.get()))).grid(row=7, column=0, columnspan=2)
        configure(self.c_frame, 8, 2)
        
    
    def clear_radio(self):
        """
        Deselect every radiobutton. 
        :return None
        """
        for children in self.winfo_children():
            if isinstance(children, ttk.Radiobutton):
                children.state(['!selected'])