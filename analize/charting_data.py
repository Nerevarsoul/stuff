import datetime
import math

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
    # new_date = [price['num_date'][0]]

    # for i in np.arange(1, len(price['num_date'])):
        # diff = price['num_date'][i] - new_date[-1]
        # if diff < 1:
           # new_date.append(price['num_date'][i])
        # else:
           # new_date.append(price['num_date'][i]-math.floor(diff)) 
             
    price['new_date'] = [price['num_date'][0] + i * .020833 for i in np.arange(len(price['num_date']))]
    # price['new_date'] = new_date
    # pd.set_option('display.max_rows', len(price))
    # print price    

    ndays = np.unique(np.trunc(price['num_date']), return_index=True)
    day_count = len(ndays[0])
    xdays =  []
    for n in np.arange(day_count):
        xdays.append(datetime.date.isoformat(num2date(ndays[0][n])))

    diff = (price['new_date'][len(price['new_date'])-1]-price['new_date'][0]) / (day_count+1)
    diff = 0.625
    print day_count
    print diff
    newdays = [price['new_date'][0] + i * diff for i in np.arange(day_count)]
    
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='both', direction='out', width=2, length=8,
                   labelsize=12, pad=8)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_xticks(newdays)
    ax.set_xticklabels(xdays, rotation=45, horizontalalignment='right')

    quotes = price[['new_date', 'O', 'L', 'H' , 'C']].dropna()
    candlestick_ohlc(ax, quotes.values, width=0.05, colorup='g', colordown='r')

    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name) 
    
