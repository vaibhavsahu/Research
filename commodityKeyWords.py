import xlrd

rootFolder = 'C:\\Users\\student\\Dropbox\\Personal\\GoogleTrendsFutures\\code\\tweet2Commodities\\'

# reads from the xls files that list the keywords for each commodity
def getCommodityKeywords(commodity):
    book = xlrd.open_workbook(rootFolder+'tweet2'+commodity+'.xlsx')
    sheet = book.sheet_by_index(0)
    keywords = sheet.col_values(0, start_rowx=0, end_rowx=None)
    keywordStrings = []
    for word in keywords:
        keywordStrings = [str(word)] + keywordStrings
    return keywordStrings
    

commodityToSymbol = {'cocoa': 'Zara', 'coffee': 7, 'copper': 'First', 'corn': '', 'cotton': '', };
