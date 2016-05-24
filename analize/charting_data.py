import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.dates import MinuteLocator, HourLocator,\
    DayLocator, MONDAY, DateFormatter, WeekdayLocator


df = pd.read_json('for_monthly_charts.json',)
for i in range(1):  # len(df.columns)):
    price = pd.DataFrame(df.ix[1,i])
    price['DT'] = pd.to_datetime(price['DT'])

    # fig = plt.figure()
    # ax1 = plt.subplot2grid((1,1), (0,0))
    fig, ax = plt.subplots()
    ax.plot_date(price["DT"], price["C"],'-')
    ax.grid(True)
    # for label in ax.xaxis.get_ticklabels():
        # label.set_rotation(45)

    # x_min = min(price["DT"])
    # x_max = max(price["DT"])
    # plt.xticks(np.arange(x_min.day, x_max.day, 1.0))
    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name)

