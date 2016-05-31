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

    ndays = np.unique(np.trunc(price['num_date']), return_index=True)
    xdays =  []
    for n in np.arange(len(ndays[0])):
        xdays.append(datetime.date.isoformat(num2date(ndays[0][n])))

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_axes([0.1, 0.2, 0.85, 0.7])
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='both', direction='out', width=2, length=8,
                   labelsize=12, pad=8)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_xticks(ndays[0])
    ax.set_xticklabels(xdays, rotation=45, horizontalalignment='right')

    for day in ndays[0]:
        q = price.loc[price['my_date'] == day]
        quotes = q[['num_date', 'O', 'H', 'L', 'C']].dropna()
        fig.subplots_adjust(bottom=0.1)
        ax = fig.add_subplot(211)
        candlestick_ohlc(ax, quotes.values, width=0.05, colorup='g', colordown='r')

    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name) 
    
