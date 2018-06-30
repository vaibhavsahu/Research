from os import listdir
from os.path import isfile, join
import os

mypath = "E:\\pythonCode\\data\\twitter"
#onlyfiles = [os.path.splitext(f)for f in listdir(mypath) if isfile(join(mypath, f))]
twitterKeywords = []
def getAllTwitterKeywords():
    onlyfiles = [os.path.splitext(f) for f in listdir(mypath) if isfile(join(mypath, f))]
    for f, _ in onlyfiles:
        twitterKeywords.append(' '.join(f.split('+')))
    return twitterKeywords

print getAllTwitterKeywords()


