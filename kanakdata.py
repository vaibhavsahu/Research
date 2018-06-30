import constants as con
import nltk
from nltk.tokenize import word_tokenize


nltk.download('punkt')
# text1 = "It's true that OR ( was the OR bamboozler in ) OR multiverse."
# listname = word_tokenize(text1)
#
# l = [x for x in listname if x not in ["OR", '(', ')']]
# print l

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

genDefinitions = dictionaryJoin([con.marketTopics, con.supplyAndDemand])

for futureName, futureDefinitionPhrase in con.futureDefinitions.iteritems():
    doneTopics = []  # keep track of those that are already done
    for topicName1, topicPhrase1 in dictionaryJoin([con.futureTopics[futureName], con.marketTopics]).iteritems():
        for topicName2, topicPhrase2 in dictionaryJoin([con.futureTopics[futureName], con.supplyAndDemand]).iteritems():  # returns a dictionary
            if not topicName1 == topicName2 and topicName1 + topicName2 not in doneTopics:
        # query = futureDefinitionPhrase.replace('$','intitle:')+' ('+topicPhrase1+') '+'('+topicPhrase2+')'
                #printName = "%s_%s_%s" % (futureName, topicName1, topicName2)
                tokenizedTopicName1 = [x for x in word_tokenize(topicName1) if x not in ['OR', '(', ')']]#word_tokenize(topicName1)
                #print topicName1
                #print type(tokenizedTopicName1)
                tokenizedTopicName2 = [x for x in word_tokenize(topicName2) if x not in ['OR', '(', ')']]
                tokenizedFutureTopicPhrase = [x for x in word_tokenize(futureDefinitionPhrase) if x not in ['OR', '(', ')', '$']]
                #print tokenizedTopicName2
                #print tokenizedFutureTopicPhrase
                for top1Word in tokenizedTopicName1:  # split string based on " " remove ( and )
                    for top2Word in tokenizedTopicName2:  # split string based on " " remove ( and )
                                    # tokenizedTopicName2 = "process topicName2 here. remove whitespace and ( )"
                                    # for top2Word in tokenizedTopicName2: # split string based on " " remove ( and )
                        twitterKeyWord = " ".join(tokenizedFutureTopicPhrase) + " " + top1Word + " " + top2Word
                        print twitterKeyWord
                #print 'type of futureDefinitionPhrase: '
                #print type(futureDefinitionPhrase)

