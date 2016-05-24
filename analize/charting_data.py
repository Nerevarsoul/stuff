import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.dates import MinuteLocator, HourLocator,\
    DayLocator, MONDAY, DateFormatter, WeekdayLocator


df = pd.read_json('for_monthly_charts.json',)
for i in range(1):  # len(df.columns)):
    price = pd.DataFrame(df.ix[1,i])
    price['DT'] = pd.to_datetime(price['DT'])

    fig, ax1 = plt.subplots()
    #fig.set_size_inches((15, 8))
    ax1.plot_date(price["DT"], price["C"], '-', label='C')

    #ax2 = ax1.twinx()
    #ax2.plot_date(price["DT"], price["L"], '-', label='L')

    #ax3 = ax1.twinx()
    #ax3.plot_date(price["DT"], price["H"], '-', label='H')

    #ax4 = ax1.twinx()
    #ax4.plot_date(price["DT"], price["O"], '-', label='O')

    #ax5 = ax1.twinx()
    #ax5.plot_date(price["DT"], price["Vol"], '-', label='Vol')
    
    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name)

