import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import date2num
from matplotlib.dates import MinuteLocator, HourLocator,\
    DayLocator, MONDAY, DateFormatter, WeekdayLocator
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

df = pd.read_json('for_monthly_charts.json',)
for i in range(1):  # len(df.columns)):
    price = pd.DataFrame(df.ix[1,i])
    price['DT'] = pd.to_datetime(price['DT'])
    price['num_date'] = price['DT'].apply(date2num)
    
    dayFormatter = DateFormatter('%d')
    quotes = price[['num_date','O','L','H','C']].dropna()

    fig, ax = plt.subplots()
    fig.set_size_inches((15,8))
    ax.xaxis.set_major_formatter(dayFormatter)
    candlestick_ohlc(ax, quotes.values, width=0.05,colorup='g',colordown='r')
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name)

