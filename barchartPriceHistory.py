from suds.client import Client
import ondemand


from suds.client import Client
import logging
from barchart import API_KEY
from barchart import getHistory
from barchart import (
    getHistory,
    getQuote,
    getFinancialHighlights,
    QUOTE_TIMESTAMP_COLS,
    QUOTE_DATE_COLS
)

# API key setup
# =============

API_KEY = "47a37b92386543a88cf038b87ef3db24"
import datetime
import pprint
import requests_cache
session = requests_cache.CachedSession(
    cache_name="cache",
    backend="sqlite",
    expire_after=datetime.timedelta(days=1)
)


session = None  # pass a None session to avoid caching queries


pp = pprint.PrettyPrinter(indent=4)

print("\nTest BarchartOnDemand API")
print("=========================\n")


# one_symbol = "IBM"
# many_symbols = ["BAC", "IBM", "GOOG", "HBAN"] # this list can be used to fill out commodities symbol
# startDate = datetime.date(year=2016, month=2, day=10)
# quote_fields = [
#     "previousTimestamp",
#     "preMarketTimestamp",
#     "afterHoursTimestamp",
#     "fiftyTwoWkHighDate",
#     "fiftyTwoWkLowDate",
#     "exDividendDate",
#     "twelveMnthPctDate",
#     "tradeSize",
#     "tick",
#     "previousLastPrice",
#     "bid",
#     "bidSize",
#     "ask",
#     "askSize",
#     "previousClose",
#     "settlement",
#     "previousSettlement",
#     "openInterest",
#     "fiftyTwoWkHigh",
#     "fiftyTwoWkLow",
#     "avgVolume",
#     "sharesOutstanding",
#     "dividendRateAnnual",
#     "dividendYieldAnnual",
#     "impliedVolatility",
#     "twentyDayAvgVol",
#     "twelveMnthPct",
#     "preMarketPrice",
#     "preMarketNetChange",
#     "preMarketPercentChange",
#     "afterHoursPrice",
#     "afterHoursNetChange",
#     "afterHoursPercentChange",
#     "averageWeeklyVolume",
#     "averageQuarterlyVolume",
#     "exchangeMargin"
# ]
#
# financial_fields = [
#     "annualNetIncome",
#     "ttmNetIncome",
#     "ttmNetProfitMargin",
#     "lastQtrEPS",
#     "ttmEPS",
#     "twelveMonthEPSChg",
#     "peRatio",
#     "recentEarnings",
#     "recentDividends",
#     "recentSplit",
#     "beta"
# ]



# # getQuote with ONE symbol
# # ========================
# print("{0} Quote".format(one_symbol))
# print("=========")
# try:
#     quote = getQuote(one_symbol, fields=quote_fields, session=session)
#     for timestamp in QUOTE_TIMESTAMP_COLS:
#         if timestamp in quote and quote[timestamp]:
#             quote[timestamp] = quote[timestamp].isoformat()
#     for datefield in QUOTE_DATE_COLS:
#         if datefield in quote and quote[datefield]:
#             quote[datefield] = quote[datefield].isoformat()
#     print(pp.pprint(quote))
# except NotImplementedError as err:
#     print("getQuote failed: {}".format(err))
#
# # getQuote with SEVERAL symbols
# # =============================
# print("\n{0} Quotes".format(many_symbols))
# print("=====================================")
# try:
#     quotes = getQuote(many_symbols, fields=quote_fields, session=session)
#     for quote in quotes:
#         for timestamp in QUOTE_TIMESTAMP_COLS:
#             if timestamp in quote and quote[timestamp]:
#                 quote[timestamp] = quote[timestamp].isoformat()
#         for datefield in QUOTE_DATE_COLS:
#             if datefield in quote and quote[datefield]:
#                 quote[datefield] = quote[datefield].isoformat()
#     print(pp.pprint(quotes))
# except NotImplementedError as err:
#     print("getQuote failed: {}".format(err))
#
#
# # # getHistory with ONE symbol
# # ==========================
# print("\nHistory of {0} since {1}".format(one_symbol, startDate))
# print("===============================")
# try:
#     history = getHistory(one_symbol, typ="daily", startDate=startDate, maxRecords=5, session=session)
#     for key, val in history.items():
#         print("Symbol: {0}".format(key))
#         for v in val:
#             print("==========================")
#             v["timestamp"] = v["timestamp"].isoformat()
#             v["tradingDay"] = v["tradingDay"].isoformat()
#             print(pp.pprint(v))
# except NotImplementedError as err:
#     print("getHistory failed: {}".format(err))
#
# # getHistory with SEVERAL symbols
# # ===============================
# print("\nHistories of {0} since {1}".format(many_symbols, startDate))
# try:
#     histories = getHistory(many_symbols, typ="daily", startDate=startDate, maxRecords=5, order="desc", session=session)
#     for key, history in histories.items():
#         print("============================================================")
#         print("Symbol: {0}".format(key))
#         for item in history:
#             print("==========================")
#             item["timestamp"] = item["timestamp"].isoformat()
#             item["tradingDay"] = item["tradingDay"].isoformat()
#             print(pp.pprint(item))
# except NotImplementedError as err:
#     print("getHistory failed: {}".format(err))



# logging.getLogger('suds.client').setLevel(logging.DEBUG)
#
# ondemand = Client('https://ondemand.websol.barchart.com/service?wsdl')
#
# #getHistroy - symbols, apikey, url_base -> "marketdata.websol.barchartondemand.com", start_date -> 20100101, end_date -> 20130101, typ, maxRecords, interval, order, session)
# r = getHistory('AAPL','47a37b92386543a88cf038b87ef3db24', "marketdata.websol.barchartondemand.com", '20100101', '20130101', 'minutes', 10, 60, 'asc', 'EFK')
# #result = getHistory('AAPL', 'minutes', '20100101', '20130101', '10', '60', 'asc', 'EFK', 'true', 'true', 'sum', '1', 'true', 'NYSE,AMEX,NASDAQ', 'false', '1', 'expiration')
#
# from suds.client import Client
# ondemand = Client('https://marketdata.websol.barchart.com/service?wsdl')
#
# result = getHistory('AAPL', 'minutes', '20100101', '20130101', '10', '60', 'asc', 'EFK')#, 'true', 'true', 'sum', '1', 'true', 'NYSE,AMEX,NASDAQ', 'false', '1', 'expiration')
#
# print result