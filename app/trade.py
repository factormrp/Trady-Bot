# hotfix for Matplotlib GUI outside main thread warning
import matplotlib
matplotlib.use('Agg')

import os
import pandas as pd
from numpy import nan
from yfinance import Ticker
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')

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
        mac10 = prices.rolling(window=10).mean()
        mac34 = prices.rolling(window=34).mean()

        # for each day in range, check for buy/sell indicator at open or close and if no open position, record price in list
        for i in range(len(prices)):
            if mac10[i] > mac34[i] and open_pos_flag != 1:
                    buys.append(prices[i])
                    sells.append(nan)
                    open_pos_flag = 1
            elif mac10[i] < mac34[i] and open_pos_flag != 0 and open_pos_flag != -1:
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
    elif strat == "Mean Reversion":
        buys,sells = None,None
        strat = "MR"
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
