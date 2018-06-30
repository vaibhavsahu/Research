#http://pandas.pydata.org/pandas-docs/dev/timeseries.html


import numpy
import pandas
import quandl
import matplotlib.pyplot as plt
from matplotlib import rcParams

# df = pandas.DataFrame( { "A": [11, 12, 13], "B": [34,78,109] } )
# print df
#
# print df.sum()
from matplotlib import pyplot
from pandas import Series

#rcParams.update({'figure.autolayout': True, 'axes.titlepad': 20})
series = Series.from_csv('E:\\COM-AG_FAB.csv', header=0, infer_datetime_format=True)
df = pandas.read_csv('E:\\COM-AG_FAB.csv', header=0, infer_datetime_format=True)
#series1 = Series.from_csv('E:\\COM-WLD_GOLD.csv')
pyplot.plot(series)
pyplot.show()

# fig = plt.figure()
# fig.show()