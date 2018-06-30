import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib as mpl


from matplotlib.finance import candlestick_ohlc


import pandas as pd

import csv

import numpy as np




marketFutures = "C:\\Users\\flannlab\\Dropbox\\GoogleTrendsFutures\\GoogleTwitterFutures_Vaibhav\\Data\\price.txt"

df = pd.read_csv(marketFutures, keep_default_na=False)


date = [i for i in df['Date']]
# closeprice = [float(i.replace(',', '')) for i in df['Price']]
# openprice = [float(i.replace(',', '')) for i in df['Open']]
# highprice = [float(i.replace(',', '')) for i in df['High']]
# lowprice = [float(i.replace(',', '')) for i in df['Low']]
closeprice = [float(i) for i in df['Price']]
openprice = [float(i) for i in df['Open']]
highprice = [float(i) for i in df['High']]
lowprice = [float(i) for i in df['Low']]
infoMeasure = [float(i) for i in df['InfoMeasure']]
#volume = [float(i.replace('K', ''))*1000 for i in df['Vol.']]#remove K and convert the value to float, and multiply by 1000

closeprice = np.array(closeprice, dtype=np.float64)
openprice = np.array(openprice, dtype=np.float64)
highprice = np.array(highprice, dtype=np.float64)
lowprice = np.array(lowprice, dtype=np.float64)
infoMeasure = np.array(infoMeasure, dtype=np.float64)

date = [mdates.datestr2num(i) for i in date]

dayFormatter = mdates.DateFormatter('%d-%b')

ohlc = []
i = 0
while(i < len(date)):
    stats_day = date[i], openprice[i], highprice[i], lowprice[i], closeprice[i], infoMeasure[i]
    ohlc.append(stats_day)
    i = i + 1

fig = plt.figure()
#fig, axl = plt.subplots()
ax1 = plt.subplot2grid((5,4),(0,0),rowspan=4,colspan=4)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(dayFormatter)
ax1.xaxis.set_major_locator(mticker.MaxNLocator(20))
candlestick_ohlc(ax1, ohlc, width=0.5, colorup='g', colordown='r', alpha=0.8)

ax1.grid(True)


ax2 = plt.subplot2grid((5,4),(4,0),sharex=ax1,rowspan=1,colspan=4)
ax2.bar(date,infoMeasure)

ax2.axes.yaxis.set_ticklabels([])
plt.ylabel('PSI')

ax2.grid(True)

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(90)
for label in ax2.xaxis.get_ticklabels():
    label.set_rotation(45)

#plt.xticks(rotation=45)
#plt.grid()
plt.xlabel('Dates')
#plt.ylabel('Prices')
#plt.title('Prices vs Information Measurement')
plt.tight_layout()

# plt.plot(date, openprice)
# plt.plot(date, closeprice)
# plt.plot(date, highprice)
# plt.plot(date, lowprice)
plt.savefig("E:\\Research\\data\\price\\OilFuture.png", dpi=200, bbox_inches='tight')
plt.subplots_adjust(left=0.09,bottom=.18,right=.94,wspace=.20,hspace=0)
plt.show()