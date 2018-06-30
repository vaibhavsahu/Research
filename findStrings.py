import re
import constants

tweetText = 'Oil demand will remain strong through at least 2020, pushing spot costs for crude above futures pricing, a BofA analyst says https://bloom.bg/2CH6Cup'


def matchAllKeywords(text, splitCharacter = " "):
    #returns the keywords that are contained in tweet
    #ignores the order of the keywords in the keywordsString
    foundList = []
    text = text.lower()
    #print keywords
    for keywords in constants.getAllCurrentKeywords():
        if matchOneKeywords(text, keywords.lower().split(splitCharacter)): 
           #print keywords
            foundList.append(keywords)
    return foundList

def matchOneKeywords(text, wordList):
    #match against all keywords
    found = True
    for oneWord in wordList:
        found = found and (text.find(oneWord) >= 0)
        if not found:
            break
    return found

#Order
##def keywordsInString(text, keywords):
##    # order dependent?
##    #<span class="str">'.*are.*'</span>
##    # so works with + or space between workds
##    regularExp = '.*' + keywords.replace('+', '.*').replace(' ', '.*') + '.*'
##    #print regularExp
##    if re.match(regularExp, text, re.M|re.I):
##        return keywords

#text='Pianegonda Sterling Silver Yellow Cross Earrings Retail $485 NEW! NO RESERVE!! http://t.co/ekwmW1e8HD http://t.co/UVdMI6IEsp'
#print matchAllKeywords(tweetText)

            
            
            
    
