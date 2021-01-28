# hotfix for Matplotlib GUI outside main thread warning
import matplotlib
matplotlib.use('Agg')

import os
import pandas as pd
from numpy import nan
from yfinance import Ticker
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')

def calculate_rsi(prices,n):
    # calculate n period differences
    ndiff = prices.diff()
    
    # calculate the exponential moving averages of all up and down changes
    ups,downs = ndiff.copy(),ndiff.copy()
    ups[ups<0] = 0
    downs[downs>0] = 0
    ups = ups.ewm(span=2).mean()
    downs = downs.abs().ewm(span=2).mean()

    # calculate rsi values
    return 100.0 - (100.0/(1.0+(ups/downs)))

def filtered_n_rsi_mean_reversion(prices,period,n=2):
    buys,sells = [],[]
    enter = 30 if n == 4 else 5
    open_pos_flag = -1
    held = 0

    try:
        # generate exponential moving averages for entry filter and rsi values
        filt50 = prices.ewm(span=50).mean()
        filt200 = prices.ewm(span=200).mean()
        rsis = calculate_rsi(prices,n)

        # for each time frame in range, check if conditions hold for entry or exit and record price when indicators trigger
        for i in range(len(prices)):
            if filt50[i] > filt200[i] and open_pos_flag != 1 and rsis[i] <= enter:
                buys.append(prices[i])
                sells.append(nan)
                open_pos_flag = 1
                held += 1
            elif rsis[i] >= 75 and open_pos_flag == 1:
                buys.append(nan)
                sells.append(prices[i])
                open_pos_flag = 0
                held = 0
            elif held > 9 and open_pos_flag == 1:
                buys.append(nan)
                sells.append(prices[i])
                open_pos_flag = 0
                held = 0
            else:
                buys.append(nan)
                sells.append(nan)
                held += 1
    except:
        print('Applying algorithm went wrong. Exiting...')
        return None,None

    return buys,sells


def dual_moving_average_crossover(prices,period):
    """ This function returns a tuple of lists with stored prices indicating when to buy and sell

    Parameters
        :param: prices - a pandas Series holding ticker open and close prices
        :param: period - a string holding keyword for desired data range

    """
    # initialize data stores and open position flag
    buys,sells = [],[]
    open_pos_flag = -1

    try:
        # generate moving average series
        sma10 = prices.rolling(window=10).mean()
        sma34 = prices.rolling(window=34).mean()

        # for each timeframe in range, check for buy/sell indicator at open or close and if no open position, record price in list
        for i in range(len(prices)):
            if sma10[i] > sma34[i] and open_pos_flag != 1:
                    buys.append(prices[i])
                    sells.append(nan)
                    open_pos_flag = 1
            elif sma10[i] < sma34[i] and open_pos_flag == 1:
                    buys.append(nan)
                    sells.append(prices[i])
                    open_pos_flag = 0
            else:
                buys.append(nan)
                sells.append(nan)
    except:
        print('Applying algorithm went wrong. Exiting...')
        return None,None

    return buys,sells

def simulate(ticker,strat,period,cash=1000):
    """ This function simulates a chosen strategy on a given ticker over the course of a specified period

    Parameters
        :param: ticker - security ticker symbol (e.g. AAPL)
        :param: strat - algorithmic trading strategy (e.g. MAC)
        :param: period - period of time from for which to run simulation (e.g YTD)
        
    Keyword Arguments
        :kwarg: cash - the principal balance of the account

    """
    # set the interval for the data query
    res = set_price_resolution(period)

    # pull ticker data for specified period and interval
    data = Ticker(ticker).history(period=period,interval=res,actions=False)

    # concatenate all open and close prices 
    prices = pd.concat([data['Open'],data['Close']]).sort_index()

    # initialize indicator stores
    buys,sells = None,None
    # apply strategy and get back buy/sell indications
    if strat == "Moving Average Crossover":
        buys,sells = dual_moving_average_crossover(prices,period)
        strat = "MAC"
    elif strat == "Breakout & Trailing Stop Loss":
        buys,sells = None,None
        strat = "BTSL"
    elif strat == "4 Period Mean Reversion":
        buys,sells = filtered_n_rsi_mean_reversion(prices,period,4)
        strat = "4MR"
    elif strat == "2 Period Mean Reversion":
        buys,sells = filtered_n_rsi_mean_reversion(prices,period)
        strat = "2MR"
    if buys is None and sells is None:
        exit()

    # Create a png of the strategy applied to ticker
    savefile = visualize(ticker,strat,period,prices,buys,sells) 
    if savefile == "error":
        exit()

    return savefile
    
def visualize(ticker,strat,period,prices,buys,sells):
    """ This function takes in a ticker, its prices, and its indicators to visualize the chosen strategy

    Parameters
        :param: ticker - string with the name of the chosen ticker
        :param: prices - pandas Series holding ticker's prices over specified period
        :param: buys - pandas Series holding chosen strategy's indications to buy
        :param: sells - pandas Series holding chosen strategy's indications to sell
    """
    # create the empty file to store png
    if not os.path.isdir('./app/static/plots'):
        os.mkdir('./app/static/plots')
    open('./app/static/plots/{}-{}-{}.png'.format(strat,ticker,period),'w').close()

    try:
        plt.figure(figsize=(8,4.5))
        plt.plot(range(len(prices)),prices,label=ticker,alpha=0.4)
        plt.scatter(range(len(prices)),buys,label='Buy',marker='^',color='green')
        plt.scatter(range(len(prices)),sells,label='Sell',marker='v',color='red')
        plt.title('{} Adjusted Price History With {} Signals'.format(ticker,strat))
        plt.legend(loc='upper left')
        plt.savefig('./app/static/plots/{}-{}-{}.png'.format(strat,ticker,period))
    except:
      print('Saving plot went wrong. Exiting...')
      return "error"
    
    return '{}-{}-{}.png'.format(strat,ticker,period)

def set_price_resolution(period):
    if period == 'ytd':
        return "1d"
    elif period[-1] == 'd':
        return '2m'
    elif period[-1] == 'o':
        return '1h'
    elif period[-1] == 'y':
        return '1d'
    else:
        return '5d'
