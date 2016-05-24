import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.dates import MinuteLocator, HourLocator,\
    DayLocator, MONDAY, DateFormatter, WeekdayLocator
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

df = pd.read_json('for_monthly_charts.json',)
for i in range(1):  # len(df.columns)):
    price = pd.DataFrame(df.ix[1,i])
    price['DT'] = pd.to_datetime(price['DT'])
    
    fig = plt.figure()
    fig.set_size_inches((335, 18))
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    ax1.plot_date(price['DT'], price['O'],'-')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.xlabel('Date')
    plt.ylabel('Price')
    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.title(name) 
    plt.legend()   

    plt.savefig(name)

