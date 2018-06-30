import urllib2
import re
import time
import random
from datetime import datetime
from sys import argv
import constants as con

#https://www.google.com/#newwindow=1&q=flu+trends&tbs=qdr:h
#keywords='coffee market price
#query='coffee+market+price'

def getQueryData(query, printName, isTest, timePeriod='d'):
    print query
    countWords = len(re.findall(r'\w+', query))
    countPages = getGooglePageCount(query, isTest, timePeriod) 
    print "%5d : %s\n\n"%(countPages,  printName)
    return (countPages, countWords)

def getGooglePageCount(keywords, isTest = False, timePeriod = 'd'):
    query = keywords.replace(' ', '+')
    #Google header custome range format
    #cdr%3A1%2Ccd_min%3A4%2F<day>%2F<year>%2Ccd_max%3A4%2F<day>%2F<year>
    #https://www.google.com/search?q=intitle:gold+futures+-jewelry*+(south+africa+OR+russia+OR+india+OR+australia)&tbs=cdr%3A1%2Ccd_min%3A4%2F1%2F2018%2Ccd_max%3A4%2F17%2F2018&tbm=
    #cdr%3A1%2Ccd_min%3A<min_month_in_numeric>%2F<min_day_in_numeric>%2F<min_year_in_numeric>%2Ccd_max%3A<max_month_in_numeric>%2F<max_day_in_numeric>%2F<max_year_in_numeric>&tbm=
    url = ('http://www.google.com/search?q=*&as_qdr='+timePeriod).replace("*", query) #h or #d
    urlWithDateRange = ('http://www.google.com/search?q=*&tbs=cdr%3A1%2Ccd_min%3A4%2F1%2F2018%2Ccd_max%3A4%2F17%2F2018&tbm=').replace("*", query)  # h or #d
    print url
    #print urlWithDateRange
    return getGoogle(url, isTest)

def getGoogle(url, isTest):
    #url = 'http://www.google.com/search?q=intitle:oil+-soybeans+(middle+east+OR+syria+OR+iraq+OR+israel+OR+Saudi+Arabia+OR+russia)+(rallied+OR+sharply+higher+OR+market+up)&tbs=qdr:w'
    if isTest:
        print "\n%s"%(url)
    headers = {'User-Agent': random.choice(con.getUserAgents())} #'Mozilla/5.0'} #headers
    if not isTest: #False: go out to google
        req = urllib2.Request(url, None, headers)
        pageString = urllib2.urlopen(req, timeout=2).read() #added time out
        #print pageString
        count = extractCount(pageString)
    else:
        count = 50
    return count #10.0/0.0 #count

def extractCount(search):
    results_re = r'About (.*?) results' #.*? to get the minimal count
    results = re.findall(results_re, search)
    print results
    if results:
        return int(results[0].replace(',', ''))
    else:
        #only one page so count the individual sites
        results = re.findall(r'www\..*?\.com', search) #match only minimal .*?, need the \. in front of com
        results1 = [x for x in results if x not in ['www.google.com', 'www.youtube.com']]
        return len(set(results1))

# print getGoogle('http://www.google.com/search?q=(intitle:"s%26p+500"+futures)+(production+OR+glut+OR+reserves+OR+exports+OR+stocks+OR+cuts+OR+inventory)+(gold+futures+-jewelry*)&tbs=qdr:w',
#                 False)
# print getGooglePageCount('q',False)
# print getGooglePageCount('(intitle:oil+-soybeans)+(crisis+OR+collapse+OR+danger+OR+slump+OR+crash)+(intitle:gold+futures+-jewelry*)&as_rq&tbs=qdr:')

##def dictionaryJoin(*args): DOES NOT WORK
##    print args
##    print
##    if len(args)==1:
##        return args[0]
##    return dictionaryMerge(args[0], dictionaryJoin(args[1:]))
##


# print getGooglePageCount('ADP Employment report less than OR greater than OR surprise OR worse than OR more than')
# print getGooglePageCount('stock earnings falls OR dissapointment OR lower OR higher OR better OR rises -drift -holding -marginally')
# print getGooglePageCount('debt crisis OR collapse OR danger OR slump OR crash')
# print getGooglePageCount('market crisis OR collapse OR danger OR slump OR crash')
# print getGooglePageCount('selling OR down OR lower OR short gold -jewelry -coins -team -medal -dresses')
# print getGooglePageCount('buying OR up OR higher OR long gold -jewelry -coins -team -medal -dresses')
# print getGooglePageCount('dollar yellen OR federal reserve OR Treasury Reserve')
#
# print getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods china demand')
# print getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods china supply')
# print getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods africa supply')
# print getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods africa supply')
# print getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods china supply')
# print getGooglePageCount('intitle:gold -jewelry* -coins* -team* -medal* -dresses* -coast* -"as gold" -watch* -jeweler* -goods* -passport* india supply')


#['india supply', 'china supply', 'mining africa', 'deposits discovered', 'forecast -weather', 'africa supply']:
#forecast OR tomorrow OR awaiting OR outlook -weather
##for i in range(0,1):
##    gold = 'intitle:gold market -jewelry* -coins* -team* -medal* -dresses* -coast* -"as gold" -watch*'
##    coffee = 'intitle:coffee futures -brew* -drink* -taste* -shop* -mugs* -cup*'
##    for marketName, marketPhrase in marketPhrases.iteritems():
##        for coffeeName, coffeePhrase in coffeeCrop.iteritems():
##            query = '('+coffeePhrase+') '+coffee+' ('+marketPhrase+')'
##            query = '('+gold+') '+marketPhrase+' ('+coffee+')'
##            print query
##            name = "coffee %s AND %s"%(coffeeName, marketName)
##            name = "coffee AND %s AND gold"%(marketName)
##            if (len(re.findall(r'\w+', query)) > 32):
##                print "number of words = %2d, name=%s\n\n"%(len(re.findall(r'\w+', query)), name)
##            count = getGooglePageCount(query) 
##            print "%5d %s"%(count, name)
##    time.sleep(random.uniform(60, 120))

#relationTopics =[('gold', 'oil', dictionaryJoin([Market, oilTopics, supplyAndDemand])),
#                  ] #List of tuples




###relation between two topics for one commodity graph
##for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems(): #(name, def phrase)
##    for generalTopicName, generalTopicPhrase in dictionaryJoin([con.marketTopics, con.supplyAndDemand]).iteritems():
##        for futureTopicName, futureTopicPhrase in con.futureTopics[futureName].iteritems(): #returns a dictionary
##            query = futureDefinitionPhrase.replace('$','intitle:')+' ('+futureTopicPhrase+') '+'('+generalTopicPhrase+')'
##            printName = "%s & %s & %s"%(futureName, futureTopicName,  generalTopicName)
##            getQueryData(query, printName)
##
###relation between two commodities for same topic
##doneFutures = [] #keep track of those that are already done
##for futureName0, futureDefinitionPhrase0 in con.futureDefinitions.iteritems(): #(name, def phrase)
##    doneFutures.append(futureName0)
##    for futureName1, futureDefinitionPhrase1 in con.futureDefinitions.iteritems(): #(name, def phrase)
##        if futureName1 not in doneFutures: #to avoid doing both directions, but should this be done because the orders are different because intitle:
##            for generalTopicName, generalTopicPhrase in dictionaryJoin([con.marketTopics, con.supplyAndDemand]).iteritems():
##                #intitle qualifier for the first commodity
##                query = '('+futureDefinitionPhrase0.replace('$','intitle:')+') '+generalTopicPhrase+' ('+futureDefinitionPhrase1.replace('$','')+')'
##                printName = "%s & %s & %s"%(futureName0, generalTopicName,  futureName1)
##                getQueryData(query, printName)

    
#if __name__ == '__main__':
#    if len(argv) < 2:
#        print 'Usage: python {} search terms'.format(argv[0])
#    else:
#        search_terms = argv[1:]
#        search_results = get_search(search_terms)
#        print search_results
#        print get_num_results(search_results)

#keywords = commodityKeyWords.getCommodityKeywords('gold')

#while True:
#    nowTime = datetime.now()
#    print nowTime.strftime('%Y/%m/%d %H:%M:%S')
#    print getPrice.get_last_price('KC', 'U', '14')
#    for keys in keywords:
#        time.sleep(1) #random.randrange(1,3)) #3,10
#        print 'Keys = {}, count = {}'.format(keys, get_num_results(get_search(keys)))
#
#    #random.shuffle(keywords)
#    print '\n'
    


