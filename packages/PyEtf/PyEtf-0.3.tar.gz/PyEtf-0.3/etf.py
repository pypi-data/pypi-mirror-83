from time import strftime
import yfinance as yf
import datetime
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import numpy as np
import os
from functions import date_from_text, nextWeekDay

class ETF:
    """Class that rapresent an ETF analizing his performance since the buying date"""

    def __init__(self, ticker, buy_date, n_shares, buy_price, commissions_ini, sell_date=None, sell_price=None, info='ETFs/', sell_commissions=0):
        """
        Initialization of the ETF
        :param ticker: ticker name (str)
        :param buy_date: date when the ETF was bought (datetime.date)
        :param n_shares: number of shares owned (int)
        :param buy_price: price at which the ETF was bought (float)
        :param commissions: amount payed to the bank (float)
        :param sell_date: optional parameter that is needed when the ETF has already been sold (datetime.date)
        :param sell_price: price at which the ETF has been sold (float)
        :param sell_commissions: amount payed to the bank when selling the ETF(float)
        :param info: other informations about the ETF (dict)
        """
        self.ticker_name = ticker
        self.buy_date = buy_date
        self.n_shares = n_shares
        self.buy_price = buy_price
        self.commissions = [commissions_ini, sell_commissions]
        self.sell_date = sell_date
        self.sell_price = sell_price
        self.info = info 
        try:
            self.ticker = yf.Ticker(self.ticker_name.split('-')[0])
        except ConnectionError:
            self.ticker = None
        self.refresh()

    def initial_value(self):
        """
        Calculates the initial value of your holding
        :return: float
        """
        return round(self.n_shares * self.buy_price, 2)

    def initial_investment(self):
        """
        Calculates the initial value of your investment: initial value + commissions 
        :return: float
        """
        return round(self.initial_value() + self.commissions[0], 2)

    def present_value(self):
        """
        Calculates the present value of your holding if it hasn't been already sold; otherwise returns 0
        :return: float
        """
        return round(self.data.iloc[-1]['Close'] * self.n_shares, 2) if not self.sold() else 0

    def sold(self):
        """
        Returns True if the ETF has already been sold, otherwise returns False
        :return: bool
        """
        return self.sell_date is not None

    def total_commissions(self):
        """
        Returns the total amount payed in commisions summing the initial and the final ones.
        :return: float
        """
        return round(sum(self.commissions), 2)

    def _PL(self):
        """
        Calculates the profit or losses realised since the buying date
        :return: float
        """
        if not self.sold():
            return round(self.present_value()- self.initial_investment(), 2)
        else:
            return round(self.n_shares * self.sell_price - self.initial_investment(), 2)
    
    def profit_loss(self, pct=False):
        """
        Calculates the profit or losses realised since the buying date express in percentage or absolute values 
        :param pct: True if percentage result, False otherwise (bool) 
        :return: float
        """
        return round(self._PL() / self.initial_investment() * 100, 2) if pct else self._PL()

    def _first_good_date(self, day):
        """
        Finds the closest date in the databse to the one given 
        :param day: (datetime.date)
        :return: datetime.date
        """
        count = 0
        while True:
            try:
                self.data.loc[day - timedelta(count)]
                return day - timedelta(count)
            except KeyError:
                count += 1

    def add_info(self, info):
        """
        Add information about the ETF
        :param info: (dict) 
        :return: None
        """
        for k, v in info.items():
            self.info[k] = v
    
    def refresh(self):
        """
        Refresh data about the ETF
        :return: None
        """
        if os.path.isfile(f'{self.info}{self.ticker_name}.csv'):
            self.data = pd.read_csv(f'{self.info}{self.ticker_name}.csv', parse_dates=True)
            str_to_date = lambda x: date(int(x.split('-')[0]),int(x.split('-')[1]),int(x.split('-')[2].split(' ')[0]))
            self.data = self.data[self.data['Date'] != self.data['Date'].shift(1)]
            self.data['Date'] = self.data['Date'].apply(str_to_date)
            self.data.set_index('Date', inplace=True)
            if self.ticker is not None and not self.sold():
                newData = self.get_new_data(self.data.index[-1])
                for row in newData.index:
                    if row in self.data.index:
                        self.data.drop(row, inplace=True)
                self.data = pd.concat([self.data, newData]) 
        else:
            if self.sold():
                self.data = self.ticker.history(start=self.buy_date, end=self.sell_date)
            else:
                self.data = self.ticker.history(start=self.buy_date)

        # Completing new stats   
        self.calculateStats()

        # if datetime.datetime.today().hour < 18 and self.data.index[-1] == date.today():
        #     self.data['OK'][-1] = False

        self.data.insert(0, 'Date', self.data.index)
        self.data.to_csv(f'{self.info}{self.ticker_name}.csv', index=False)
    
    def calculateStats(self):
        self.data['Prev Close'] = self.data['Close'].shift(1)
        self.data['Var%'] = self.data['Close'].pct_change() * 100
        self.data['Var_from_Ini_%'] = (self.data['Close'] - self.data['Close'][0]) / self.data['Close'][0] * 100
        self.data['Profit/Loss'] = self.data['Close'] * self.n_shares - self.initial_investment()
        if self.sold():
            self.data.loc[self.sell_date:, 'Profit/Loss'] = self.sell_price * self.n_shares - self.initial_investment()
        self.data['Present_Value'] = self.data['Close'] * self.n_shares
        self.data['Invested'] = self.initial_investment()
        self.data['OK'] = True

    def get_new_data(self, startDate):
        """
        Estract date from yahoo finance based on the start date and returns them.
        :param startDate: datetime.date
        :return pd.DataFrame
        """
        newData = self.ticker.history(start=startDate)
        newData['Date'] = newData.index
        newData['Date'] = newData['Date'].apply(lambda x: x.date())
        newData.set_index('Date', inplace=True)
        idx = list(newData.index)
        if len(idx) > 1:
            if idx[-1] == idx[-2]:
                idx[-1] = nextWeekDay(idx[-1])
            newData.index = idx
        if '.' in self.ticker_name:
            country = self.ticker_name.split('-')[0].split('.')[1]
        else:
            country = 'NY'
        if country == 'L':
            EURGBP = yf.Ticker('GBPEUR=X').history(start=date.today()).iloc[-1]['Close']
            newData[['Open','High','Low','Close']] = newData[['Open','High','Low','Close']] * EURGBP
        elif country == 'NY':
            EURUSD = yf.Ticker('EURUSD=X').history(start=date.today()).iloc[-1]['Close']
            newData[['Open','High','Low','Close']] = newData[['Open','High','Low','Close']] / EURUSD
        return newData

    def sell(self, sell_date, sell_price, commissions):
        """
        Add information about the selling of the ETF. Sets the sell date to the one passad as a parameter
        as well as the price. Add the commissions to the existing ones.
        :param sell_date: (datetime.date)
        :param sell_price: (float)
        :param commissions: (float) 
        :return: None
        """
        self.sell_date = sell_date
        self.sell_price = sell_price
        self.commissions[1] = commissions
        self.refresh()

    def stock_price(self, day='today'):
        """
        Returns the stock price on a given date. As default the date is set to the last one occured 
        :param day: (datetime.date)
        :return: float
        """
        if day != 'today' and day < self.buy_date:
            return 'Date not in Database'
        if self.sold() and (day == 'today' or day > self.sell_date):
            return 0
        return round(self.data.loc[self._first_good_date(day), 'Close'],2) if day != "today" else round(self.data['Close'][-1],2)

    
    def get_gain(self, day='today', pct=False):
        """
        Get the gain or loss made by the ETF on a given day
        :param info: (datetime.date) 
        :return: float
        """
        if day == 'today':
            day = self.data.index[-1]
        day = self._first_good_date(day)
        if (not self.sold() and day > self.buy_date) or (self.sold() and self.sell_date > day > self.buy_date):
            if pct:
                return round(self.data.loc[day, 'Var%'], 2)
            else:
                return round((self.data.loc[day, 'Close'] - self.data.loc[day, 'Prev Close']) * self.n_shares, 2) 
        else:
            return 'Invalid Date'

    def get_value(self, day='today'):
        """
        Gets the value of the position on a given date
        :param day: (datetime.date)
        :return: float
        """
        if day == 'today':
            if self.sold():
                return 0
            day = self.data.index[-1]
        if (not self.sold() and day > self.buy_date) or (self.sold() and self.sell_date > day > self.buy_date):
            return round(self.data.loc[self._first_good_date(day), "Close"] * self.n_shares, 2)
        else:
            return 0

    def gains_btw_dates(self, date_ini, date_fin='today', pct=False):
        """
        Calculates the gains (absolute or percentage) of the ETF during the selcted period
        :param date_ini: (datetime.date)
        :param date_fin: (datetime.date)
        :param pct: (bool)
        :return: float
        """
        if date_fin == 'today':
            date_fin = self.data.index[-1]
        date_ini = self._first_good_date(date_ini) - timedelta(1)
        date_fin = self._first_good_date(date_fin)
        if pct:
            return round((self.get_value(date_fin) - self.get_value(date_ini)) / self.get_value(date_ini) * 100, 2)
        else:
            return round(self.get_value(date_fin) - self.get_value(date_ini), 2)

    def mean(self):
        """
        Returns the percentage mean of the Var % 
        :return: float
        """
        return round(self.data['Var%'].mean(),2)   

    def median(self):
        """
        Returns the percentage median of the Var % 
        :return: float
        """
        return round(self.data['Var%'].median(), 2)

    def equity_line(self, sp500=False, pct=True):
        """
        Draws an historical series about the price of the ETF. If the sp500 parameter is True, the graph of the
        Standard & Poor 500 is added. If the pct parameter is True results will be in percentage form.
        :param pct: bool
        :param sp500: bool
        :return: None
        """
        spy = None 
        if sp500:
            if not self.sold():
                spy = yf.Ticker("SPY").history(start=self.buy_date)
            else:
                spy = yf.Ticker("SPY").history(start=self.buy_date, end=self.sell_date)
        fig = plt.figure(figsize=(4,2), dpi=200)
        fig.patch.set_facecolor('#ececec')
        ax = fig.add_subplot(111)
        if pct:
            ax.plot(self.data['Var_from_Ini_%'], color="green", label=self.ticker_name, lw=1.2)
            ax.set_ylabel("Var (%)")
            if sp500:
                spy['Var%'] = (spy.Close - spy.Close[0]) / spy.Close[0] * 100
                ax.plot(spy['Var%'], color="orange", label="SPY", linewidth=1.2)
        else:
            ax.plot(self.data['Close'], lw=1.2, color="green", label=self.ticker_name)
            if sp500:
                divisor = spy.Close[0] / self.data.Close[0]
                ax.plot(spy['Close'] / divisor, lw=1.2, color="orange", label="SPY")
            ax.set_ylabel("Price (€)")
        ax.set_title(f"{self.ticker_name} - Daily")
        ax.set_xlabel("Time")
        ax.xaxis.set_major_locator(dates.MonthLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%b-%Y'))
        ax.grid(True)
        fig.autofmt_xdate()
        ax.legend()
        return fig, ax
    
    def bar_chart(self, period):
        """
        Draws a bar chart showing the historical returns based on the chosen period. Available periods are:
        "W" --> for a weekly chart
        "M" --> for a monthly chart
        "Y" --> for a yearly chart
        :param period: W - M - Y (str)
        :return: None
        """
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
        periods = {"M": ("Monthly","Months"), "Y": ("Yearly", "Years"), "W": ("Weekly", "Weeks")}
        sample = pd.concat([self.data.head(1), self.data.resample(period).last()])
        sample['Var%'] = sample['Close'].pct_change() * 100
        if period == "W":
            d = [x for x in sample.index.week[1:]]
        elif period == "M":
            d = [months[x-1] for x in sample.index.month[1:]]
        elif period == "Y":
            d = [x for x in sample.index.year[1:]]
        else:
            d = None
        sample.dropna(inplace=True)
        colors = sample['Var%'].apply(lambda x: "green" if x > 0 else "red")
        index = np.arange(len(sample['Var%']))
        fig = plt.figure(figsize=(8,4), dpi=250)
        fig.patch.set_facecolor('#ececec')
        ax = fig.add_axes([0,0,1,1])
        ax.bar(index, sample['Var%'], 0.35, color=colors, alpha=1, label=f"{periods[period][0]} Statistics")
        ax.set_xlabel(periods[period][1])
        ax.set_ylabel("Var (%)")
        ax.set_title(f"{periods[period][0]} Profit / Loss %")
        ax.set_xticks(index)
        ax.set_xticklabels(d, fontsize=6)
        ax.grid(True, alpha=0.5)
        fig.autofmt_xdate()
        ax.legend()
        return
    
    def box_plot(self):
        """
        Draws a box plot of the percentage variation of the ETF since the buying date.
        :return: None
        """
        fig = plt.figure(figsize=(8,4), dpi=250)
        ax = fig.add_axes([0,0,1,1])
        ax.boxplot(self.data.dropna()['Var%'], vert=True, patch_artist=True)
        ax.set_xlabel(self.ticker_name)
        ax.set_ylabel("Var (%)")
        ax.set_title(f"{self.ticker_name} - Box Plot Var %")
        ax.set_xticks([0])
        ax.set_xticklabels([""])
        ax.grid(True, alpha=0.5)
        return 

    def __str__(self):
        string = f"Ticker: {self.ticker_name}  --->  Comprato il: {str(self.buy_date)}"
        string += f"\nNumber of shares: {self.n_shares}"
        string += f"\nPrice per share: {self.buy_price} €"
        string += f"\nCommissions: {self.commissions[0]+ self.commissions[1]} €"
        string += "\n"
        string += f"\nInitial Investment: {self.initial_investment()} €"
        string += f"\nPresent Value: {self.present_value()} €"
        string += f"\nPresent Stock Price: {round(self.stock_price(), 2)} €"
        string += f"\nProfit/Loss: {self.profit_loss()} €"
        string += f"\nProfit/Loss (%): {self.profit_loss(pct=True)} %\n"
        return string      