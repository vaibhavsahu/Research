# the utility of this file is to hit Google for queries just once in a day to avoid HTTP error 503.
#and save the retrieved results in a cache.
# Rule to update the cache or use the cache will be based on the timestamps. If the timestamps are older than 24 hrs or a day
#we would need to rehit the Google for queries.
#format for caching the results??

import graphRelations as gr
import generateAllQueries as gaq
import searches as srch



srch.getGooglePageCount('ADP Employment report less than OR greater than OR surprise OR worse than OR more than')
srch.getGooglePageCount('stock earnings falls OR dissapointment OR lower OR higher OR better OR rises -drift -holding -marginally')
srch.getGooglePageCount('debt crisis OR collapse OR danger OR slump OR crash')
srch.getGooglePageCount('market crisis OR collapse OR danger OR slump OR crash')
srch.getGooglePageCount('selling OR down OR lower OR short gold -jewelry -coins -team -medal -dresses')
srch.getGooglePageCount('buying OR up OR higher OR long gold -jewelry -coins -team -medal -dresses')
srch.getGooglePageCount('dollar yellen OR federal reserve OR Treasury Reserve')

srch.getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods china demand')
srch.getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods china supply')
srch.getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods africa supply')
srch.getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods africa supply')
srch.getGooglePageCount('intitle:gold -jewelry -coins -team -medal -dresses -coast -"as gold" -watch -jeweler -goods china supply')
srch.getGooglePageCount('intitle:gold -jewelry* -coins* -team* -medal* -dresses* -coast* -"as gold" -watch* -jeweler* -goods* -passport* india supply')
#
# #Generate All Queries
globalPrintNames, comTopcomQueryName, comTopTopQueryName, comTopQueryName = gaq.generateQueries()
#
# _, printNameCTC =  comTopcomQueryName
# _, printNameCTT = comTopTopQueryName
# _, printNameCT =  comTopQueryName

#feed google queries here
#for
# print comTopcomQueryName
# print comTopTopQueryName
# print comTopQueryName

#Plot the correlatoion graphs
#gr.generateGraph(True, 'phraseTopics')




