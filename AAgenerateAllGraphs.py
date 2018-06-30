from os import listdir
from os.path import isfile, join
import constants as con
import glob
import re
import arrow
import graphRelations as gr

#dataType = 'google'
dataType = 'twitter'
dirName = con.ROOTdata + dataType + '\\'
#onlyFiles = [ f for f in listdir(dirName) if isfile(join(dirName,f

files = glob.glob(dirName + "real*@*.txt")
files.sort()
for fileName in files:
    dayTimes = re.findall(r'_d_.*?\.txt', fileName)
    if not dayTimes == []:
        string = dayTimes[0]
        timeString = string[3:22]
        gr.generateGraph(False, timeString)
        print timeString
'real_d_2014_09_23@23_15_52.txt'


              
