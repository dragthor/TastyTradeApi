import TastyTradeApi
import asyncio
import time

from DXFeed import *


tickers = [ "SPY" ]

liveTradingEnabled = False


async def main():
    email = ""
    password = ""
    apiUrl = ""
    authToken = ""
    userName = ""

    async def quote_callback(result):
        ticker = result["data"][1][0] # Quote
        bid = float(result["data"][1][6]) # bidPrice
        ask = float(result["data"][1][10]) # askPrice
        print(ticker + " - mid: " + str(midpoint(bid, ask)) + ", bid: " + str(bid) + ", ask: " + str(ask))

    def midpoint(bid, ask):
        return round((bid + (ask - bid) / 2), 2)

    settings = TastyTradeApi.readLocalConfig("tastytrade.ini")
    email = settings["email"]
    password = settings["password"]
    apiUrl = settings["apiUrl"]

    authToken = TastyTradeApi.getSessionAuthorizationToken(apiUrl, email, password)

    if len(authToken) == 0:
        print("Unable to get Tastytrade authorization token.")

    userName = TastyTradeApi.validateSession(apiUrl, authToken)

    if len(userName) == 0:
        print("Unable to validate Tastytrade session.")

    streamerTokens = TastyTradeApi.getStreamerTokens(apiUrl, authToken)

    dxFeedToken = streamerTokens["token"]
    streamerUrl = streamerTokens["streamer-url"]
    websocketUrl = streamerTokens["websocket-url"] + "/cometd"

    tt_dxfeed = DXFeed(websocketUrl, dxFeedToken)

    await tt_dxfeed.connect()

    # Utilize getFutureStreamerSymbols (or getEquityStreamerSymbol) for proper symbol.
    # items = TastyTradeApi.getFutureStreamerSymbols(apiUrl, authToken, tickers[0])
    items = TastyTradeApi.getEquityStreamerSymbol(apiUrl, authToken, tickers[0])

    #print(items)

    await tt_dxfeed.subscribe([DXEvent.QUOTE], tickers)

    seconds = 10
    t_end = time.time() + seconds
    
    while time.time() < t_end:
        await tt_dxfeed.listen(quote_callback)

    await tt_dxfeed.disconnect()

    closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

    if closeResult != 204:
        print("Unable to close/kill Tastytrade session.")


asyncio.run(main())
