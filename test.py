# coding: utf-8
import ahocorasick
import constants
import re


tree = ahocorasick.KeywordTree()

for keyword in constants.getAllCurrentKeywords():
    for word in keyword.split('+'):
        if word:
            tree.add(word)
tree.make()

tag = '<p> Crude oil does have some bullish fundamentals with craziness going on in Iraq and the fact that economies around the world are improving especially here in the United States with the unemployment number coming out adding another 288,000 jobs as high gas prices are here to stay in my opinion, but as a trader I have to look for a breakout to enter or exit while right now the trend is neutral.  </p>'

for (start, end) in tree.findall(tag):
    print tag[start:end]

allKeywords = constants.getAllCurrentKeywords()

reAll = '.*' + allKeywords[0].replace('+', '.*') + '.*'
matcher = re.compile(reAll)
for keywords in constants.getAllCurrentKeywords()[1:]:
    regularExp = '.*' + keywords.replace('+', '.*') + '.*'
    matcher.compile(regularExp)

matcher = re.compile(reAll)
for m in matcher.finditer(tag):
    print '%02d-%02d: %s' % (m.start(), m.end(), m.group(0))
# print r
# for one in r:
#     print one.groups()

tree.add("alpha")
tree.add("alpha beta")
tree.add("gamma")
##>>>
tree.make()
##>>>
tree.search("I went to alpha beta the other day to pick up some spam")

