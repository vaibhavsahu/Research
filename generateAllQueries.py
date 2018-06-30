import random
import constants as con
import searches
from random import shuffle
from nltk.tokenize import word_tokenize
import nltk


nltk.download('punkt')

def generateQueries(onlyCommoditiesList = ['gold', 'oil', 'stockMarket']):
    #returns a list of tuples (query printName)
    # print name can be used to parse the components of the query for the graph
    comTopcomQueryName = []
    comTopTopQueryName = []
    comTopQueryName = []
    #make a global list of printNames extracted during compilation of  comTopcomQueryName, comTopTopQueryName, comTopQueryName
    globalListPrintNames = []
    allTopics = dictionaryJoin([con.marketTopics, con.supplyAndDemand])
    #relation between general and  topics for one commodity graph
##    for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems(): #(name, def phrase)
##        for generalTopicName, generalTopicPhrase in dictionaryJoin([con.marketTopics, con.supplyAndDemand]).iteritems():
##            for futureTopicName, futureTopicPhrase in con.futureTopics[futureName].iteritems(): #returns a dictionary
##                query = futureDefinitionPhrase.replace('$','intitle:')+' ('+futureTopicPhrase+') '+'('+generalTopicPhrase+')'
##                printName = "%s_%s_%s"%(futureName, futureTopicName,  generalTopicName)
##                comTopTopQueryName.append((query, printName)) #getQueryData(
    #relations between general and general for one commodity
    #set twitter or google to true depending upon type of data
    googleKey = True
    twitterKey = False
    genDefinitions = dictionaryJoin([con.marketTopics, con.supplyAndDemand])
    # HERE WE SPECIALIZE TO ONLY WORK WITH THE GIVEN COMMODITY
    # COM TOP TOP
    for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems():
        if futureName in onlyCommoditiesList:
            doneTopics = []  # keep track of those that are already done
            for topicName1, topicPhrase1 in dictionaryJoin([con.futureTopics[futureName], con.marketTopics]).iteritems():
                for topicName2, topicPhrase2 in dictionaryJoin([con.futureTopics[futureName], con.supplyAndDemand]).iteritems():  # returns a dictionary
                    if not topicName1 == topicName2 and topicName1 + topicName2 not in doneTopics:
                        if googleKey:
                            query = futureDefinitionPhrase.replace('$','intitle:')+' ('+topicPhrase1+') '+'('+topicPhrase2+')'
                            printName = "%s_%s_%s" % (futureName, topicName1, topicName2)
                            globalListPrintNames.append((futureName, printName))
                            #print (futureName, printName)
                            comTopTopQueryName.append((query, printName))
    
                        if twitterKey:
                        # tokenizedTopicName1 = [x for x in word_tokenize(topicName1) if x not in ['OR', '(', ')']]  # word_tokenize(topicName1)
                            tokenizedTopicPhrase1 = [x for x in word_tokenize(topicPhrase1) if x not in ['-buy','$', '-jewelry*', '-soybeans*','-brew*', '-brew*', '-drink*', '-shop*', '-cotton*', '-cocoa*', '-drink', '-cotton', '-coffee', 'OR', '(', ')', '``', '-weather', '-sell', '-short', '-hold*', '-long', '-covering', '-holding', '-drift', '-steady', "''"]]  # word_tokenize(topicName1)
                            tokenizedTopicPhrase2 = [x for x in word_tokenize(topicPhrase2) if x not in ['-buy','$', '-jewelry*', '-soybeans*','-brew*', '-brew*', '-drink*', '-shop*', '-cotton*', '-cocoa*', '-drink', '-cotton', '-coffee', 'OR', '(', ')', '``', '-weather', '-sell', '-short', '-hold*', '-long', '-covering', '-holding', '-drift', '-steady', "''"]]
                            tokenizedFutureTopicPhrase = [x for x in word_tokenize(futureDefinitionPhrase) if x not in ['-buy','$', '-jewelry*', '-soybeans*','-brew*', '-brew*', '-drink*', '-shop*', '-cotton*', '-cocoa*', '-drink', '-cotton', '-coffee', 'OR', '(', ')', '``', '-weather', '-sell', '-short', '-hold*', '-long', '-covering', '-holding', '-drift', '-steady', "''"]]
                            # tokenizedTopicName2 = [x for x in word_tokenize(topicName2) if x not in ['OR', '(', ')']]
                            # tokenizedFutureTopicPhrase = [x for x in word_tokenize(futureDefinitionPhrase) if x not in ['OR', '(', ')', '$']]
                            for top1Word in tokenizedTopicPhrase1:  # split string based on " " remove ( and )
                                for top2Word in tokenizedTopicPhrase2:  # split string based on " " remove ( and )
                                    # tokenizedTopicName2 = "process topicName2 here. remove whitespace and ( )"
                                    # for top2Word in tokenizedTopicName2: # split string based on " " remove ( and )
                                    twitterKeyWord = " ".join(tokenizedFutureTopicPhrase) + " " + top1Word + " " + top2Word
                                    #print twitterKeyWord
                                    comTopTopQueryName.append((twitterKeyWord, printName))
    
                                #print printName
                        #comTopTopQueryName.append((twitterKeyWord, printName)) #getQueryData(
                        #twitterKeyWord, printName) this tuple can be used in graphs for side by side comparison with google data.
                        #however, we are feeding just set of keywords to twitter. make a list of keywords from broken down queries.
                        #this list can further be used to pass to twitter stream listeners
                    doneTopics+=[topicName2+topicName1, topicName1+topicName2]
    # relation between one commodity and its topics
    # COM TOP
    for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems(): #(name, def phrase)
        if futureName in onlyCommoditiesList:
            for topicName, topicPhrase in dictionaryJoin([con.futureTopics[futureName], genDefinitions]).iteritems():
                query = futureDefinitionPhrase.replace('$','intitle:')+' ('+topicPhrase+')'
                printName = "%s_%s"%(futureName, topicName)
                globalListPrintNames.append((futureName, printName))
                #print (futureName, printName)
                #print query
                comTopQueryName.append((query, printName)) #getQueryData(
    #relation between two commodities for same topic
    # COM TOP COM
    doneFutures = [] #keep track of those that are already done
    if len(onlyCommoditiesList) > 1:
        for futureName0, futureDefinitionPhrase0 in con.futureDefinitions.iteritems(): #(name, def phrase)
            if futureName0 in onlyCommoditiesList:
                for futureName1, futureDefinitionPhrase1 in con.futureDefinitions.iteritems(): #(name, def phrase)
                    if futureName1 in onlyCommoditiesList:
                        if not [] == [ (f0,f1) for f0, f1 in con.futurePairs if f0==futureName0 and f1==futureName1]:
                            for generalTopicName, generalTopicPhrase in dictionaryJoin([con.marketTopics, con.supplyAndDemand]).iteritems():
                                #intitle qualifier for the first commodity
                                query = '('+futureDefinitionPhrase0.replace('$','intitle:')+') ('+generalTopicPhrase+') ('+futureDefinitionPhrase1.replace('$','')+')'
                                printName = "%s_%s_%s"%(futureName0, generalTopicName,  futureName1)
                                globalListPrintNames.append((futureName0, printName))
                                #print (futureName0, printName)
                                comTopcomQueryName.append((query, printName))
                            doneFutures.append([futureName0+futureName1, futureName1+futureName0])
    #print comTopcomQueryName
    # for query, printName in comTopcomQueryName:#co
    #     print query
    #print "Generated %d comTopCom Q"%(len(comTopcomQueryName))
    #print "Generated %d comTopTop Q"%(len(comTopTopQueryName))
    #print "Generated %d comTop Q"%(len(comTopQueryName))
    return (globalListPrintNames, comTopcomQueryName, comTopTopQueryName, comTopQueryName)

def dictionaryJoin(topics):
    #topics is a list of directories
    dictJoin = topics[0]
    for oneTopic in topics[1:]:
        dictJoin = dictionaryMerge(dictJoin, oneTopic)
    return dictJoin

def dictionaryMerge(a,b):
    c = a.copy()
    c.update(b)
    return c

_, comTopcomQueryName, comTopTopQueryName, comTopQueryName = generateQueries()
# _, printNameCTC =  comTopcomQueryName
# _, printNameCTT = comTopTopQueryName
# _, printNameCT =  comTopQueryName
# print comTopcomQueryName
# print comTopTopQueryName
# print comTopQueryName


#comTopcomQueryName, comTopTopQueryName, comTopQueryName = generateQueries()
#for query, printName in comTopcomQueryName:
#    print "%-25s %s"%(printName, query)
##    #searches.getQueryData(query, printName)
