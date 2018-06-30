import constants
import tweepy
import urllib2
import re
import time
import constants
import arrow
from datetime import datetime
from bs4 import BeautifulSoup
import dataManage
import findStrings
from collections import Counter
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from twitterAuthorization import getTwitterAuthorization

#create a API
#http://stackoverflow.com/questions/14250359/obtain-all-followers-ids-of-a-user-from-twitter-using-correct-pagination

#user = api.get_user('@FuturesTrader71')
#print user.id

def getTwitterIDs():
    auth = getTwitterAuthorization()
    api = tweepy.API(auth)
    urlRoot = 'http://commodityhq.com/2012/100-insightful-futures-traders-worth-following-on-twitter/'
    headers = {'User-Agent': 'Mozilla'}
    requestRoot = urllib2.Request(urlRoot, None, headers)
    topPage = urllib2.urlopen(requestRoot).read()
    #print topPage
    #print '**** parsed ****'
    parsed = BeautifulSoup(topPage, 'html.parser')
    #print parsed
    #print '**** tags ****'
    tags = parsed.find_all("a")
    #pattern_twitter_username = '@([A-Za-z0-9_]+)'
    tags = parsed.find_all("a") # tags is not returning list of <a> tags inside <ol> or <li> tags. vaibhav
    #updated_tags = parsed.find_all(pattern_twitter_username)
    #print tags
    pattern = '>@.*<'

    theseKeywords = []
    userIDs = []
    userNames = []
    for tag in tags:
    #for tag in tags:
        #print tag
        tagString = tag.encode('utf-8') # dont use tag.string!
        #print tagString
        userNameString = re.findall(pattern, tagString)
        #print  '***************** userNameString **************************'
        print userNameString
        if userNameString:
            userName = userNameString[0].replace('<','').replace('>','')
            print userName
            try:
                user = api.get_user(str(userName))
                print user, user.id
                print '{} -> {}'.format(userName, user.id)
                userIDs.append(user.id)
                userNames.append(userName)
            except:
                pass
    return [str(u) for u in userIDs]

#http://commodityhq.com/2012/100-insightful-futures-traders-worth-following-on-twitter/
#userIDs.append(str(api.get_user(str(status.author.screen_name)).id))
#http://stackoverflow.com/questions/13215054/tweepy-public-stream-filter-by-a-changing-variable
            
userIDs = getTwitterIDs()
#userIDs.append(str(api.get_user(str(status.author.screen_name)).id))
print userIDs


