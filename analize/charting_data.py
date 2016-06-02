import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from pylab import date2num
from matplotlib.dates import MinuteLocator, HourLocator, num2date,\
    DayLocator, MONDAY, DateFormatter, WeekdayLocator
from matplotlib.finance import candlestick_ohlc


df = pd.read_json('for_monthly_charts.json',)
for i in range(1):  # len(df.columns)):
    price = pd.DataFrame(df.ix[1,i])
    price['DT'] = pd.to_datetime(price['DT'])
    price['num_date'] = price['DT'].apply(date2num)
    price['my_date'] = np.trunc(price['num_date'])
    price['new_date'] = [price['num_date'][0] + i * .020833 for i in np.arange(len(price['num_date']))]
    # print price    

    ndays = np.unique(np.trunc(price['num_date']), return_index=True)
    xdays =  []
    for n in np.arange(len(ndays[0])):
        xdays.append(datetime.date.isoformat(num2date(ndays[0][n])))

    newdays = np.unique(np.trunc(price['new_date']), return_index=True)

    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='both', direction='out', width=2, length=8,
                   labelsize=12, pad=8)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_xticks(newdays[0])
    ax.set_xticklabels(xdays, rotation=45, horizontalalignment='right')

    quotes = price[['new_date', 'O', 'L', 'H' , 'C']].dropna()
    candlestick_ohlc(ax, quotes.values, width=0.05, colorup='g', colordown='r')

    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name) 
    
