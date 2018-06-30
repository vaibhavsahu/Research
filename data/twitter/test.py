import matplotlib.pyplot as plt
import csv
import pandas
#
# x = []
# y = []
#
# with open('E:\\agent_State.csv','r') as csvfile:
#     #csvfile = csvfile.next()
#     plots = csv.reader(csvfile, delimiter=',')
#     plots = [row for row in plots][1:]
#
# print plots
#
# plt.plot(x,y, label='Loaded from file!')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()

df = pandas.read_csv('E:\\agent_State.csv')

print df

for index, row in df.iteritems():
    print row['Clostridium1']