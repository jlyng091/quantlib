import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup

# when obtaining data from numerous sources, we want to standardise communication units
# object-types should be the same. dataframe 'index' types or classes should be the same

import datetime
def format_date(dates):
    yymmdd = list(map(lambda x: int(x), str(dates).split(' ')[0].split('-')))
    # take a list of dates in [yy-mm-dd (other stuff)] format and 
    # strip away the other stuff to return a datetime object
    return datetime.date(yymmdd[0], yymmdd[1], yymmdd[2])

def get_sp500_instruments():
    res = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    return list(df[0]['Symbol'])

# symbols = get_sp500_instruments()
# print(symbols)

# let's get ohlcv data
def get_sp500_df():
    symbols = get_sp500_instruments()
    symbols = symbols[:30]              # limit to first 30 stocks
    ohlcvs = {}
    for sym in symbols:
        sym_df = yf.Ticker(sym).history(period='10y')
        # print(sym_df)
        ohlcvs[sym] = sym_df[['Open', 'High', 'Low', 'Close', 'Volume']].rename(
            columns={
                'Open':'open',
                'High':'high',
                'Low':'low',
                'Close':'close',
                'Volume':'volume'
            }
        )

    df = pd.DataFrame(index=ohlcvs['AMZN'].index)
    df.index.name = 'date'
    instruments = list(ohlcvs.keys())

    for inst in instruments:
        inst_df = ohlcvs[inst]
        # adding a column identifier
        columns = list(map(lambda x: '{} {}'.format(inst, x), inst_df.columns))
        # add instrument names to table
        df[columns] = inst_df

        # print(df)
    return df, instruments

# df, instruments = get_sp500_df()
# df.to_excel('sp500_data.xlsx')
# print(instruments)

# take an arbitrary dataframe with "inst o/h/l/c/v" and append data + other numerical stats
# for use throughout the system
def extend_dataframe(traded, df):
    # first put all the date strings into datetime format
    df.index = pd.Series(df.index).apply(lambda x: format_date(x))
    open_cols = list(map(lambda x: str(x) + ' open', traded))
    high_cols = list(map(lambda x: str(x) + ' high', traded))
    low_cols = list(map(lambda x: str(x) + ' low', traded))
    close_cols = list(map(lambda x: str(x) + ' close', traded))
    volume_cols = list(map(lambda x: str(x) + ' volume', traded))

    historical_data = df.copy()
    print(historical_data)
    historical_data = historical_data[open_cols + high_cols + low_cols + close_cols + volume_cols]
    historical_data.fillna(method='ffill', inplace=True)
    
    for inst in traded:
        # let's get return statistics using closing prices
        # and volatility statistics using rolling stdev of 25-day windows
        # also check if a stock is actively traded
        historical_data['{} % ret'.format(inst)] = historical_data['{} close'.format(inst)] \
            / historical_data['{} close'.format(inst)].shift(1) - 1
        
        historical_data['{} % ret vol'.format(inst)] = historical_data['{} % ret'.format(inst)].rolling(25).std()
        historical_data['{} active'.format(inst)] = historical_data['{} close'.format(inst)] \
            != historical_data['{} close'.format(inst)].shift(1)

    historical_data.fillna(method='backfill', inplace=True)
    
    return historical_data

# df, instruments = get_sp500_df()
# historical_data = extend_dataframe(instruments, df)

# print(historical_data)
# historical_data.to_excel('hist.xlsx')

# used backfill and forwardfill to deal with NAs... swap other methods as needed
# alternate methods include:
"""
1. Forwardfill then Backfill
2. Brownian motion / Brownian Bridge
3. GARCH. GARCH variants + copulas
4. Synthetic data, such as thru GANs and stochastic volatility neural nets
Select based on approaches. Try former for backtesting and latter for training neural models.
"""

# will switch out this data module for a dependency on a brokerage
# so data can come from external sources (e.g. scraping) and we can implement a common
# data structure to pass between different components of the quant system
# entire teams can be dedicated to obtaining/cleaning/processing/learning/manipulating data
