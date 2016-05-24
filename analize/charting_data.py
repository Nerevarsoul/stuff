import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_json('for_monthly_charts.json',)
for i in range(len(df.columns)):
    price = pd.DataFrame(df.ix[1,i])
    price['DT'] = pd.to_datetime(price['DT'])
    plt.plot(price["DT"], price["C"])
    name = "{}-{}.png".format(price['DT'][0].year, price['DT'][0].month)
    plt.savefig(name)
