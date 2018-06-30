import numpy as np
import matplotlib.pyplot as plt
import os
import time

fileRoot = 'C:\Users\student\Dropbox\ResearchBioEngineering\data\\'
patchSizes = ['400']#, '300', '200', '100']
hours = ["{0:0>3}".format(i) for i in range(1, 73)] #CHANGE

def eliminateZeros(data):
    # replaces all 0.0 values with a neighboring non-zero value
    change = True
    while change:
        change = False
        for ((x,y), value) in np.ndenumerate(data):
            if value == 0.0:
                for (xD, yD) in neighbors():
                    try:
                        if not data[x+xD, y+yD] == 0.0:
                            data[x,y] = data[x+xD, y+yD]
                            change = True
                    except:
                        pass
    return data

#list of von Newman neighbors
def neighbors():
    for i in range(-1,2):
        for j in range(-1,2):
            if not i == 0 and not j == 0:
                yield(i, j)

#START SCRIPT
files = []
for patch in patchSizes:
    for hour in hours:
        fileName = fileRoot + 'Patch' + patch + '_VEGF\VEGF solute ' + hour
        files.append(fileName)
        
##maxValue = 0
##previousData = eliminateZeros(np.loadtxt(files[0] + '.txt'))
##for fileName in files[1:]:
##    data = eliminateZeros(np.loadtxt(fileName + '.txt'))
##    maxValue = max(maxValue, (data - previousData).max())
##print maxValue
#maxValue = 4.2868299608989877e-05 #precompute for all files





previousData = np.zeros([257, 257])
for fileName in files:
    data = eliminateZeros(np.loadtxt(fileName + '.txt'))
    #data = np.loadtxt(fileName + '.txt')
    print data.sum()-previousData.sum()
    fig = plt.imshow(data-previousData, interpolation='none',origin='upper',aspect = 1,
                     cmap = 'jet')#, vmin = 0.0, vmax = maxValue) 
    plt.gca().grid(False)
    #fig.set_cmap('jet')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(fileName + '.png', bbox_inches='tight', dpi=200)
    plt.clf()
    previousData = data

print "DONE\n"


##            
##max(data100.max(), data400.max())
##
##fileName100 = 'C:\Users\student\Dropbox\ResearchBioEngineering\data\VEGF solute 072_100' 
##data100 = np.loadtxt(fileName100 + '.txt')
##fileName400 = 'C:\Users\student\Dropbox\ResearchBioEngineering\data\VEGF solute 072_400' 
##data400 = np.loadtxt(fileName400 + '.txt')
##
##maxValue = max(data100.max(), data400.max())
##fig = plt.imshow(data100/maxValue, interpolation='none',origin='upper',aspect = 1) #extent=[0,howMany,0,len(keywordList)])
##plt.gca().grid(False)
##fig.set_cmap('jet')
##fig.axes.get_xaxis().set_visible(False)
##fig.axes.get_yaxis().set_visible(False)
##cbar = plt.colorbar('jet')
##plt.savefig(fileName100 + '.png', bbox_inches='tight', dpi=200)
##plt.clf()
##fig = plt.imshow(data400/maxValue, interpolation='none',origin='upper',aspect = 1) #extent=[0,howMany,0,len(keywordList)])
##plt.gca().grid(False)
##fig.set_cmap('jet')
##fig.axes.get_xaxis().set_visible(False)
##fig.axes.get_yaxis().set_visible(False)
##plt.savefig(fileName400 + '.png', bbox_inches='tight', dpi=200)
##
