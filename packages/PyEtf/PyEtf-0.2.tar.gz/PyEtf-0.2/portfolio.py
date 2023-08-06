import os
from etf import ETF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import matplotlib.dates as dates
from datetime import datetime
from datetime import date, timedelta
import matplotlib.pylab as pylab

class Portfolio:
    """Class representing a portfolio of ETFs and his performances during time"""

    INFO = 'Info.csv'

    def __init__(self):
        """
        Class initialization. The paramter neeeded is refering to the info file.
        :param info_file: str
        :return: None 
        """    
        params = {'axes.titlesize': 'xx-large', 'axes.labelsize': 6, 'font.size':6}
        pylab.rcParams.update(params)
        self.etfs = {}
        if os.path.isfile(self.INFO):
            f = pd.read_csv(self.INFO, parse_dates=True)
            for x in f.index:
                if not isinstance(f.loc[x, 'sell_date'], str):
                    self.etfs[f.loc[x, 'Name']] = ETF(f.loc[x, 'Name'],datetime.strptime(f.loc[x, 'buy_date'],'%Y-%m-%d').date(),
                    f.loc[x, 'n_shares'],f.loc[x, 'buy_price'], f.loc[x, 'commissions_ini'])
                else:
                    self.etfs[f.loc[x, 'Name']] = ETF(f.loc[x, 'Name'],datetime.strptime(f.loc[x, 'buy_date'],'%Y-%m-%d').date(),
                    f.loc[x, 'n_shares'],f.loc[x, 'buy_price'],f.loc[x, 'commissions_ini'],datetime.strptime(str(f.loc[x, 'sell_date']),'%Y-%m-%d').date(),
                    f.loc[x, 'sell_price'],f.loc[x, 'info'],f.loc[x, 'sell_commissions'])
        else:
            os.makedirs('ETFs')
            info = pd.DataFrame(columns=['Name','buy_date','n_shares','buy_price','commissions_ini','sell_date','sell_price','info','sell_commissions'])
            info.to_csv(self.INFO, index=False)
        self.data = pd.DataFrame()
        if len(self.etfs) != 0:
            self.refresh()
    
    def add_etf(self, etf):
        """
        Function for adding a new ETF to the portfolio
        :param etf: ETF
        :return: None 
        """ 
        assert isinstance(etf, ETF), 'Error! You have to pass an ETF object as an argument'
        self.etfs[etf.ticker_name] = etf
        f = pd.read_csv(self.INFO, parse_dates=True)
        f.loc[len(f)] = [etf.ticker_name,etf.buy_date,etf.n_shares, etf.buy_price, etf.commissions[0],etf.sell_date, etf.sell_price, etf.info,  etf.commissions[1]]
        f.to_csv(self.INFO, index=False)
        self.refresh()
    
    def sell_etf(self, etf_name, sell_date, sell_price, commissions):
        """
        Function for selling an ETF from the portfolio
        :param etf_name: str
        :param sell_date: datetime.date
        :param sell_price: float
        :param commissions: float
        :return: None 
        """ 
        assert etf_name in self.etfs.keys(), 'ETF not in portfolio'
        assert isinstance(sell_date, date), 'Sell_date parameter needs to be a datetime.date instance'
        assert isinstance(sell_price, float), 'Sell_price must be float'
        assert isinstance(commissions, float), 'Commissions must be float'
        self.etfs[etf_name].sell(sell_date, sell_price, commissions)
        new_file = pd.read_csv(self.INFO, index_col='Name')
        new_file.loc[etf_name, 'sell_date'] = sell_date
        new_file.loc[etf_name, 'sell_price'] = sell_price
        new_file.loc[etf_name, 'sell_commissions'] = commissions
        new_file.to_csv(self.INFO)
        self.refresh()

    def remove_etf(self, etf_name):
        """
        Function for deleting an ETF from the portfolio
        :param etf_name: str
        :return: None 
        """ 
        assert etf_name in self.etfs.keys(), 'ETF not in portfolio'
        self.etfs.pop(etf_name)
        new_file = pd.read_csv(self.INFO, index_col='Name').drop(etf_name,axis=0)
        new_file.to_csv(self.INFO)
        os.remove(f'ETFs/{etf_name}.csv')
        self.refresh()
        
    def invested_amount(self):
        """
        Calculates amount that was invested by summing every etf's initial investment.
        :return: float 
        """
        return self.data['Invested'][-1]      
    
    def profit_loss(self, pct=False):
        """
        Calculates the profit or loss accumulated since the beginning of the investments. 
        If pct is True the result will be in percentage
        :param pct: float
        :return: float 
        """
        assert isinstance(pct, bool), 'Error! The pct parameter must be boolean.'
        return round(self.data['Profit/Loss%'][-1], 2) if pct else round(self.data['Profit/Loss'][-1], 2)
    
    def get_etfs_list(self):
        """
        Print the list of ETFs present in your portfolio
        :return: str 
        """
        return " - ".join(self.etfs.keys())

    def get_etf_by_name(self, ticker):
        """
        Returns the ETF object corrsponding to the given ticker. Remember that at the end of the ticket name a "-"
        and a number ar added. Check the etfs list to be sure about the names.
        : param ticker: str
        :return: ETF
        """
        try:
            return self.etfs[ticker]
        except KeyError:
            raise KeyError(f'<{ticker}> ticker not in Portfolio. Check "get_etf_list" to get the full list of ETFs.')

    def _first_good_date(self, day):
        """
        Finds the closest date in the databse to the one given 
        :param day: datetime.date
        :return: datetime.date
        """
        count = 0
        while True:
            try:
                self.data.loc[day - timedelta(count)]
                return day - timedelta(count)
            except KeyError:
                count += 1

    def gains(self, day='today', pct=False):
        """
        Get the gain or loss made by the Portfolio on a given day
        :param day: datetime.date
        :param pct: bool
        :return: float
        """
        assert day == 'today' or isinstance(day, date), 'Error! You have to pass a datetime.date istance to the day parameter.'
        assert isinstance(pct, bool), 'Error! The pct parameter must be boolean.'
        if day == 'today':
            day = self.data.index[-1].date()
        assert self.data.index[-1].date() >= day >= self.data.index[0].date(), 'Invalid Date'
        day = self._first_good_date(day)
        if day == self.data.index[0].date():
            return round(self.data.loc[day, 'Profit/Loss%'], 2) if pct else round(self.data.loc[day, 'Profit/Loss'], 2) 
        else:
            return round(self.data.loc[day, 'Gains%'], 2) if pct else  round(self.data.loc[day, 'Gains'], 2)
    
    def value(self, day='today'):
        """
        Gets the value of the portfolio on a given date.
        :param day: datetime.date
        :return: float
        """
        assert day == 'today' or isinstance(day, date), 'Error! You have to pass a datetime.date istance to the day parameter.'
        if day == 'today':
            day = self.data.index[-1].date()
        if self.data.index[-1].date() >= day >= self.data.index[0].date():
            day = self._first_good_date(day)
            return round(self.data.loc[day, 'Value'], 2)
        else:
            return 0
    
    def gains_btw_dates(self, date_ini, date_fin='today', pct=False):
        """
        Calculates the gains (absolute or percentage) of the Portfolio during the selcted period
        :param date_ini: datetime.date
        :param date_fin: datetime.date
        :param pct: bool
        :return: float
        """
        assert date_fin == 'today' or isinstance(date_fin, date), 'Error! You have to pass a datetime.date istance to date parameters.'
        assert isinstance(date_ini, date), 'Error! You have to pass a datetime.date istance to date parameters.'
        assert isinstance(pct, bool), 'Error! The pct parameter must be boolean.'
        if date_fin == 'today':
            date_fin = self.data.index[-1].date()
        assert date_ini >= self.data.index[0].date(), 'Error ! Invalid Initial Date'
        assert date_fin >= self.data.index[0].date(), 'Error ! Invalid Final Date'
        date_fin = self._first_good_date(date_fin)
        if date_ini == self.data.index[0].date():
            profit = self.data.loc[date_fin, 'Profit/Loss']
        else:
            #date_ini = self._first_good_date(self._first_good_date(date_ini) - timedelta(1))
            date_ini = self._first_good_date(date_ini - timedelta(1))
            profit = self.data.loc[date_fin, 'Profit/Loss'] - self.data.loc[date_ini, 'Profit/Loss']
        if pct:
            return round(profit / self.value(date_ini) * 100, 2)
        else:
            return round(profit, 2)
    
    def equity_line(self, sp500=False, pct=False):
        """
        Draws an historical series about the Portfolio's gains. If the sp500 parameter is True, the graph of the
        Standard & Poor 500 is added. If the pct parameter is True results will be in percentage form.
        :param pct: bool
        :param sp500: bool
        :return: None
        """
        assert isinstance(sp500, bool), 'Error! The sp500 parameter must be boolean.'
        assert isinstance(pct, bool), 'Error! The pct parameter must be boolean.'
        #Download Standard and Poors 500 data
        spy = None
        if sp500:
            spy = yf.Ticker("SPY").history(start=self.data.index[0])

        # Plot the graph
        fig = plt.figure(figsize=(4, 2), dpi=200)
        ax = fig.add_subplot(111)
        ax.set_xlabel('Time')
        if pct:
            ax.plot(self.data['Profit/Loss%'], lw=1.2, color="blue", label='Equity')
            ax.set_title('Profit/Loss % - Daily')
            ax.set_ylabel('P/L %')
            if sp500:
                spy['Var%'] = (spy.Close - spy.Close[0]) / spy.Close[0] * 100
                ax.plot(spy['Var%'], color="orange", label="SPY", linewidth=1.2)
        else:
            ax.plot(self.data['Profit/Loss'], lw=1.2, label='Equity')
            ax.set_ylabel('Gains (€)')
            ax.set_title('Profit/Loss (€) - Daily')
        ax.xaxis.set_major_locator(dates.MonthLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%b-%Y'))
        ax.grid(True)
        fig.autofmt_xdate()
        ax.legend()
        return fig, ax
    
    def _get_marks(self, investment=True):
        """
        Return two dataframes:
        inv dataframe --> points where there was a new investment in the Portfolio considering the day before and after the investment.
        marks dataframe --> points where there was a new investment 
        :return tuple of pd.DataFrame
        """
        inv = pd.DataFrame(index=self.data.index)
        inv['Invested'] = np.where((self.data['Invested'] != self.data['Invested'].shift(1)) |
                            (self.data['Invested'] != self.data['Invested'].shift(-1)), self.data['Invested'], np.nan)
        inv.dropna(inplace=True)
        marks = pd.DataFrame(index=inv.index)
        marks['Marks'] = np.where(inv['Invested'] == inv['Invested'].shift(1), round(inv['Invested'].shift(-1) - inv['Invested'],2), np.nan)
        marks['Marks'][0] = inv['Invested'][0]
        marks['Invested'] = inv['Invested']
        marks.dropna(inplace=True)
        if investment:
            return inv, marks
        else:
            return marks

    def investment_line(self):
        """
        Draws an historical series about the amount invested in the Portfolio.
        Markers indicate how much was added each time. 
        :return: None
        """
        inv, marks = self._get_marks()
        fig = plt.figure(figsize=(4, 2), dpi=200)
        ax = fig.add_subplot(111)
        ax.plot(inv['Invested'], lw=1.2, color="blue", label='Invested', marker="o", markersize=3, markerfacecolor="grey")
        ax.set_xlabel('Time')
        ax.set_ylabel('Investments (€)')
        ax.set_title('Investment Amount (€) - Daily')
        ax.xaxis.set_major_locator(dates.MonthLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%b-%Y'))
        for x, y, mark in zip(marks.index, marks['Invested'], marks['Marks']):
            a = ax.get_ylim()
            if x == marks.index[0]:
                ax.annotate(str(mark) + " €", xy=(x + timedelta(abs((self.data.index[0] - self.data.index[-1]).days) / 80), y + (a[1]-a[0])/35), fontsize=5)
            else:
                ax.annotate(str(mark) + " €", xy=(x + timedelta(abs((self.data.index[0] - self.data.index[-1]).days) / 50), y - (a[1]-a[0])/35), fontsize=5)
        ax.grid(True)
        fig.autofmt_xdate()
        ax.legend()
        return fig, ax
    
    def value_line(self):
        """
        Draws an historical series about the Portfolio's value.
        Markers indicate how much was added or sold. 
        :return: None
        """
        marks = self._get_marks(False)
        marks['Val'] = self.data['Value']
        fig = plt.figure(figsize=(4,2), dpi=200)
        ax = fig.add_subplot(111)
        ax.plot(self.data['Value'], alpha=0.8, lw=1.2, color="green", label='Value')
        ax.scatter([x.date() for x in marks[marks['Marks']>0].index], marks[marks['Marks']>0]['Val'], marker='^', s=20, c="b", label="Buy")
        ax.scatter([x.date() for x in marks[marks['Marks']<0].index], marks[marks['Marks']<0]['Val'], marker='v', s=20, c="r", label="Sell")
        ax.set_xlabel('Time')
        ax.set_ylabel('Portfolio\'s Value (€)')
        ax.set_title('Portfolio\'s Value (€) - Daily')
        ax.xaxis.set_major_locator(dates.MonthLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%b-%Y'))
        for x, y, mark in zip(marks.index, marks['Val'], marks['Marks']):
            a = ax.get_ylim()
            if x == marks.index[0]:
                ax.annotate(str(mark) + " €", xy=(x + timedelta(abs((self.data.index[0] - self.data.index[-1]).days) / 80), y + (a[1]-a[0])/35), fontsize=5)
            else:
                if mark > 0:
                    ax.annotate(str(mark) + " €", xy=(x + timedelta(abs((self.data.index[0] - self.data.index[-1]).days) / 60), y - (a[1]-a[0])/35), fontsize=5)
                else:
                    ax.annotate(str(mark) + " €", xy=(x - timedelta(abs((self.data.index[0] - self.data.index[-1]).days) / 15), y + (a[1]-a[0])/35), fontsize=5)
        ax.grid(True)
        fig.autofmt_xdate()
        ax.legend()
        return  fig, ax
    
    def bar_chart(self, period='M', annot=True):
        """
        Draws a bar chart of the Portfolio's gains grouped by the selected period. 
        You can choose between:
        "W" --> weekly period
        "M" --> monthly period
        "Y" --> yearly period
        If the 'annot' parameter is set to True, gains or losses are shown on the chart.
        :param period: str
        :param annot: bool
        :return: None
        """
        assert period in ["W", "M", "Y"], "Wrong Period. Chose between 'W' - 'M' - 'Y'"
        assert isinstance(annot, bool), 'Error! Annot parameter must be boolean'
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        periods = {"M": ("Monthly","Months"), "Y": ("Yearly", "Years"), "W": ("Weekly", "Weeks")}
        sample = pd.concat([self.data.head(1), self.data.resample(period).last()])
        sample['Var%'] = (sample['Profit/Loss'] - sample['Profit/Loss'].shift(1)) / sample['Value'].shift(1) * 100 
        sample.dropna(inplace=True)
        colors = sample['Var%'].apply(lambda x: "green" if x > 0 else "red")
        fig = plt.figure(figsize=(4,2), dpi=200)
        ax = fig.add_subplot(111)
        ax.set_xlabel(periods[period][1])
        ax.set_ylabel("Var (%)")
        ax.set_title(f"{periods[period][0]} Profit / Loss %")
        ax.bar(np.arange(len(sample)), sample['Var%'], 0.35, color=colors, alpha=1, label=f"{periods[period][0]} Statistics")
        ax.set_xticks(np.arange(len(sample)))
        if period == "Y":
            labels = [x for x in sample.index.year]
            ax.set_ylim(sample['Var%'].min()-2,sample['Var%'].max()+2)  
        elif period == "W":
            sample_M = pd.concat([self.data.head(1), self.data.resample("M").last()])
            ax.set_xticks(np.arange(0, len(sample), 4))
            labels = [m + "-" + y for m, y in zip([months[x-1] for x in sample_M.index.month], [str(x) for x in sample_M.index.year])]
            labels[0] = months[months.index(labels[0][:-5]) - 1] + labels[0][-5:]
        else:
            labels = [m + "-" + y for m, y in zip([months[x-1] for x in sample.index.month], [str(x) for x in sample.index.year])]
        ax.set_xticklabels(labels)
        cords = {'M': (0.2, 0.5, 4, 1), 'W': (0.5, 0.5, 'x-small', 1), 'Y': (0.045, 0.3, 'x-large', 0.85)}
        if annot:
            for d, v in zip(range(len(sample)), sample['Var%']):
                if v > 0:
                    ax.annotate(str(round(v, 2)) + " %", xy=(d - cords[period][0], v+cords[period][1]), fontsize=cords[period][2])
                else:
                    ax.annotate(str(round(v, 2)) + " %", xy=(d - cords[period][0], v-cords[period][3]), fontsize=cords[period][2])
        if period != "Y":
            fig.autofmt_xdate()
        ax.grid(True, alpha=0.5)
        ax.legend()
        return fig, ax

    def pie_chart(self, pct=True, day='today'):
        """
        Draws a pie chart about the Portfolio' composition in the selected date. 
        :param pct: bool
        :param day: datetime.date
        :return: None
        """
        assert isinstance(pct, bool), 'Error! The pct parameter must be boolean.'
        assert day == 'today' or isinstance(day, date), 'Error! You have to pass a datetime.date istance to the day parameter.'
        def func(pct, allvals):
            """Funciton for the lambda function. Returns the formatted value of each ETF"""
            return str(format(round(pct/100.*np.sum(allvals), 2),".2f")) + "€"
        vals = {}
        for name, etf in self.etfs.items():
            if etf.get_value(day) != 0:
                if name.split('-')[0].split('.')[0] in vals:
                    vals[name.split('-')[0].split('.')[0]] += etf.get_value(day)
                else:
                    vals[name.split('-')[0].split('.')[0]] = etf.get_value(day)
        wgt_values = [round(v, 2) for v in vals.values()]
        explode = [0 if x != max(wgt_values) else 0.06 for x in wgt_values]
        fig = plt.figure(figsize=(4,2), dpi=200)
        ax = fig.add_subplot(111)
        if pct:
            wedges, texts, autotexts = ax.pie(wgt_values, explode=explode, labels=vals.keys(), autopct='%1.1f%%')
            plt.setp(autotexts, size=5)
        else:
            wedges, texts, autotexts = ax.pie(wgt_values, explode=explode, labels=vals.keys(), 
                                        autopct=lambda pct: func(pct, wgt_values), pctdistance=0.7)
            plt.setp(autotexts, size=4)
        plt.setp(texts, size=7, family='monospace')
        ax.set_title('Portfolio\'s Composition', size='large', color='red', weight='bold')
        return fig, ax
    
    # Just a try
    def scatter_plot(self):
        fig = plt.figure(figsize=(10, 4), dpi=300)
        ax = fig.add_axes([0,0,1,1])
        ax.scatter(self.data['Gains%'], self.data['Gains%'].shift(1))

    def investments_table(self):
        """
        Create a table showing statistic for each investment.
        :return pandas.DataFrame
        """
        table = pd.DataFrame(index=[etf.buy_date for etf in self.etfs.values()])
        table['Ticker'] = [name.split('-')[0].split('.')[0] for name in self.etfs.keys()]
        table['Buying Price (€)'] = [etf.buy_price for etf in self.etfs.values()]
        table['Number of Shares'] = [etf.n_shares for etf in self.etfs.values()]
        table['Commissions (€)'] = [etf.total_commissions() for etf in self.etfs.values()]
        table['Invested (€)'] = [etf.initial_investment() for etf in self.etfs.values()]
        table['Share Price (€)'] = [etf.stock_price() for etf in self.etfs.values()]
        table['Value (€)'] = [etf.present_value() for etf in self.etfs.values()]
        table['P/L (€)'] = [etf.profit_loss() for etf in self.etfs.values()]
        table['P/L (%)'] = [etf.profit_loss(pct=True) for etf in self.etfs.values()]
        return table

    def portfolio_table(self):
        """
        Creates a table showing statistics for each ETF type
        :return pandas.DataFrame
        """
        idx = set(name.split('-')[0].split('.')[0] for name, etf in self.etfs.items() if not etf.sold())
        table = pd.DataFrame({'Invested': 0, 'Shares':0, 'Share Price':0, 'Present Value':0, 'P/L':0, 'P/L%':0},index=idx)
        for name, etf in self.etfs.items():
            if not etf.sold():
                table.loc[name.split('-')[0].split('.')[0], 'Invested'] += etf.initial_investment()
                table.loc[name.split('-')[0].split('.')[0], 'Shares'] += etf.n_shares
                table.loc[name.split('-')[0].split('.')[0], 'Share Price'] = etf.stock_price()
                table.loc[name.split('-')[0].split('.')[0], 'Present Value'] += etf.present_value()
                table.loc[name.split('-')[0].split('.')[0], 'P/L'] += etf.profit_loss()
        table.insert(1, 'PMA', round(table['Invested'] / table['Shares'], 2))
        table.insert(3, 'Initial Weight', round(table['Invested'] / table['Invested'].sum() * 100, 2))
        table.insert(4, 'Present Weight', round(table['Present Value'] / table['Present Value'].sum() * 100, 2))
        table['P/L%'] = round(table['P/L'] / table['Invested'] * 100, 2)
        table['P/L'] = round(table['P/L'], 2)
        table['Present Value'] = round(table['Present Value'], 2)
        return table.sort_values('Invested', 0, ascending=False)
    
    def last_day_table(self):
        """
        Creates a table showing statistics for each ETF type about the last trading day
        :return pandas.DataFrame
        """
        idx = set(name.split('-')[0].split('.')[0] for name, etf in self.etfs.items() if not etf.sold()).union(['Total'])
        table = pd.DataFrame({'Value':0, 'P/L':0, 'P/L%':0},index=idx)
        if len(self.etfs) > 0:
            for name, etf in self.etfs.items():
                if not etf.sold():
                    table.loc[name.split('-')[0].split('.')[0], 'P/L'] += etf.get_gain()
                    table.loc[name.split('-')[0].split('.')[0], 'Value'] += etf.get_value(date.today()-timedelta(1))
            table['P/L%'] = round(table['P/L'] / table['Value'] * 100, 2)
            table.loc['Total', 'P/L'] = table['P/L'].sum()
            table.loc['Total', 'P/L%'] = self.gains(pct=True)
            return table.sort_values('Value', 0, ascending=False)

    def refresh(self):
        """
        Updates the data about every ETF in Portfolio, calculating Profit/Loss - Invested Amount - Profit/Loss% - Value -
        Gains - Gains%
        :return: None
        """
        # Get Profit/Loss series
        p_l = pd.DataFrame()
        for name, etf in self.etfs.items():
            p_l[name] = etf.data['Profit/Loss']
        p_l.fillna(method='ffill', inplace=True)
        self.data['Profit/Loss'] = p_l.sum(axis=1)

        # Get Invested amount seires
        inv = pd.DataFrame()
        for name, etf in self.etfs.items():
            inv[name] = etf.data['Invested']
            if etf.sold():
                inv.loc[etf.sell_date:,name] = -etf.profit_loss()
        inv.fillna(method='ffill', inplace=True)
        self.data['Invested'] = inv.sum(axis=1)

        self.data['Profit/Loss%'] = self.data['Profit/Loss'] / self.data['Invested'] * 100 # Calculates the Profit/Loss (%)
        self.data['Value'] = self.data['Invested'] + self.data['Profit/Loss']
        self.data['Gains'] = self.data['Profit/Loss'] - self.data['Profit/Loss'].shift(1)
        self.data['Gains%'] = self.data['Gains'] / self.data['Value'].shift(1) * 100
