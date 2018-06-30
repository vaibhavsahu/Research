import xlrd

from random import shuffle

#keys for Authentication TWITTER
consumer_key= 'ytwg4fSktfnqbktUIkhlaWggQ'
consumer_secret= 'bghGFrViwWuu8FCcIsEJ1oVVjDmE8ykbLR6nPaNES2w4qX3yor'
access_token= '744048595-zYPiN2KQGsVaxFrp4dv6hJkTYuUHk2M212hI5Q3Y'
access_token_secret= 'eve4jM5eakqdi7nXe0HeKKpsGNEmqtcnX37soBPc4DN9z'

ROOT = 'C:\\Python27\\'
ROOTcode = ROOT + 'pythonCode\\'
# There were windows os permission issue while writing queried data to data directory.
# I moved the data directory to E:\Research\data path
ROOTdata = 'E:\\Research\\' + 'data\\'

#thresholds
thresholdList = [0.0, 0.025, 0.05, 0.075, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]

#months
monthCodes = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z']
monthCodeToNumber = dict()
for i in range(0,12):
    monthCodeToNumber[monthCodes[i]] = i+1

def monthCode(number):
    return monthCodes[number-1]
def monthNumber(code):
    return monthCodeToNumber[code]

#commodity names and symbols ZW error, silver error, ZC, corn, silver, wheat
allCommodityNames =      ['gold', 'sugar', 'cocoa', 'hogs',  'cotton', 'orangejuice', 'coffee', 'stockMarket', 'soybeans',  'oil', 'copper', 'palladium', 'platinum']
allCommoditySymbols =    ['GC',   'SB',    'CC',    'HE',        'CT',     'OJ',          'KC',     'ES',      'ZS',    'CL',  'HG',     'PA',        'PL']
allCommodityMonths = [    [2, 4, 6, 7, 8, 9, 10, 12],\
                          [3, 5, 7, 10 ],\
                          [3, 5, 7, 9, 12],\
                          [2, 4, 5, 6, 7, 8, 10, 12],\
                          [],\
                          [],\
                          [],\
                          [],\
                          [],\
                          [],\
                          [],\
                          [],\
                          [],\
                          ] 
symbolToNameStore = dict()
symbolToMonthsStore = dict()
nameToSymbolStore = dict()

for i in range(len(allCommoditySymbols)):
    symbolToNameStore[allCommoditySymbols[i]] = allCommodityNames[i]
    symbolToMonthsStore[allCommoditySymbols[i]] = map(monthCode,allCommodityMonths[i])
    nameToSymbolStore[allCommodityNames[i]] = allCommoditySymbols[i]
    
def symbolToName(symbol):
    return symbolToNameStore[symbol]
def nameToSymbol(name):
    print nameToSymbolStore
    return nameToSymbolStore[name]
def symbolToMonths(symbol):
    return symbolToMonthsStore[symbol]


#commodity trading months
#works with xml data on commodities and contracts

import constants

rootFolder = 'C:\\Users\\student\\Dropbox\\Personal\\GoogleTrendsFutures\\code\\tweet2Commodities\\'

commodityToKeywords = dict() #with a space between the words

#FILE
# reads from the xls files that list the keywords for each commodity
def getAllKeywordsFile(commoditySymbol):
    commodityName = constants.symbolToName(commoditySymbol)
    book = xlrd.open_workbook(rootFolder+'tweet2'+commodityName+'.xlsx')
    sheet = book.sheet_by_index(0)
    keywords = sheet.col_values(0, start_rowx=0, end_rowx=None)
    #print keywords
    keywordStrings = []
    for keyword in keywords:
        #print keyword
        keyword = keyword.strip()
        #print keyword
        keywordStrings = [keyword.encode('utf-8').strip(' ')] + keywordStrings
    return keywordStrings 


#FAST LOOKUP
#commodity based keywords
def getCommodityKeywordsQuery(commoditySymbol):
    return [w.replace(' ','+').rstrip('+') for w in commodityToKeywords[commoditySymbol]] 

def getCommodityKeywords(commoditySymbol):
    return commodityToKeywords[commoditySymbol]

#all keywords
def getAllCurrentKeywordsQuery():
    #all the queries (+) irrespective of the commodity
    return [w.replace(' ','+') for w in getAllCurrentKeywords()]
    
def getAllCurrentKeywords():
    #all the keywords irrespective of the commodity
    allWords = []
    for commoditySy in allCommoditySymbols:
        for keywords in getCommodityKeywords(commoditySy):
            allWords = allWords + [keywords]
    #join together
    return list(set(allWords))

#list of updated User-Agents
#https://perishablepress.com/list-all-user-agents-top-search-engines/
def getUserAgents():
    return [

    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',

    'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
    'Mozilla/5.0',
    'Mozilla 5.10',
    'Mozilla/5.0 (Windowsshuffle; U; MSIE 9.0; Windows NT 9.0; en-US)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) Firefox/3.5.8',
    'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    ]

#FUTURES FUTURES FUTURES FUTURES FUTURES FUTURES FUTURES FUTURES FUTURES
# note intitle qualifier replaces the $
futureDefinitions = { 'gold'      :   '$gold futures -jewelry*', # -coins* -team* -medal* '#-dresses* -coast* -"as gold" -watch*'
                      #  'palladium' :   '$palladium (market OR futures)',
                      'oil'       :   '$oil futures -soybeans*',
                      'stockMarket':   '$\"stock market\"', #$\"s%26p 500\" OR $s%26p500 index
                      # 'coffee':   '$coffee futures -brew* -drink* -shop*  -cotton* -cocoa*',
                      # 'hogs':     '$(hogs OR hog) futures',
                      #   'cocoa':     'cocoa futures -drink -cotton -coffee' #NOT intitle, too little volume
                        }#-brew* '#-drink* -taste* -shop* -mugs* -cup*'



futurePairs     =   [('oil', 'gold'),
                     ('oil', 'stockMarket'),
                     ('cocoa', 'stockMarket'),
                     ('stockMarket', 'gold'),
                     ('cocoa', 'gold')
                     ]




futureTopics = {#'coffee':      {  'crop':     'bean crop (conditions OR losses OR harvest OR record)',
                  #                 'weather':  'weather OR frost OR freeze OR storm OR drought',
                  #                 'places':   'brazil OR indonesia OR vietnam OR columbia OR ethiopia'
                  #              },
                  # 'cocoa':        { 'crop':     'crop (conditions OR losses OR harvest OR record)',
                  #                 'weather':  'weather OR frost OR freeze OR storm OR drought',
                  #                 'places':   'ivory coast OR indonesia OR ghana OR liberia'
                  #                    },
                'oil':         {   'opec':   'opec (price OR news OR meeting OR eia)',
                                   'places': 'middle east OR syria OR iraq OR israel OR iran OR Saudi Arabia OR russia'
                                  },
                'gold':        {  'mine':    'mining (discovery OR strike OR speculation OR newport)',
                                  'places':  'south africa OR russia OR india OR australia'
                                 },
                'stockMarket':  {  'market': 'economy OR bear OR bull OR open (lower OR higher) OR Yellen OR stimulus',
                                  'places': 'China  OR Russia* OR Syria* OR Europe OR \"middle east\"',
                                  'other': '(Trade war OR (Bonds OR Notes) (buying OR higher)) OR hedge fund selloff OR oil lower',
                                  },
                # 'hogs':         { 'producers': 'producers OR slaughter OR packers OR feed OR virus',
                #                   'supply': 'pork over supply OR lower sales OR higher exports*',
                #                   'demand': 'pork high demand OR increased sales OR higher imports*',
                #                  },
                # 'palladium':    { 'market': 'automotive OR PAL OR SWC OR Norilsk OR Anglo Platinum OR LDI OR emissions',
                #                   'places': 'mine* (russia OR south africa) OR demand (china OR india or brazil)',
                #                  }
                 }
#TOPICS
marketTopics = { 'change3+':   'surged OR rallied OR sharply higher OR soars ',
                  'change1-':   'Lower OR decline OR downside OR fear OR -steady -drift -holding',
                  'change2-':   '(fell OR falling OR dropped) sharply OR plummets',
                  'change3-':   'panic OR tumbling OR crisis OR collapse OR danger OR slump OR crash OR plummets OR correction',
                 #
                  'action1+':   "buy OR long OR buy OR \"short covering\" OR -short",
                  'action2-':   'strong sell OR go short OR shorting OR -hold -long -covering -buy',
                  'action2+':   'strong buy OR go long OR enter long OR -hold -short -sell',

                 # 'change*+':     'rise OR increase OR strong OR up'
                 }

supplyAndDemand = {
              'production':     'production OR glut OR reserves OR exports OR stocks OR cuts OR inventory OR deficit',
               'forecast':       'forecast OR report OR outlook OR tomorrow OR projection OR news OR -weather',
               # 'eBola':          'ebola (outbreak OR dead OR economic losses OR strop travel OR emergency)',
                                  }


def randomDelayTimes():
    return [i/10 for i in [0]] #11,     13,     17,   19,     23,     29,    31]] #,     37,     41,     43]]
#,     47,    53,     59,     61,     67,     71]] #, 
     #73,     79,     83,     89,     97,    101, 103,    107,    109,    113,
    #127,    131,    137,    ,139,    149,    151]]

#I could not figure out any way to generate twitter keywords except for this
def getAllCurrentKeywords():
    return ['gold futures', 'cocoa futures', 'coffee futures', 'palladium futures', 'oil futures', 'hogs futures', 'stock market']








