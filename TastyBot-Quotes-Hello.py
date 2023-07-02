import TastyTradeApi
import asyncio
import json

from DXFeed import *


ticker = "MES"

liveTradingEnabled = False


async def main():
    email = ""
    password = ""
    apiUrl = ""
    authToken = ""
    userName = ""

    async def quote_callback(result):
        bid = float(result["data"][1][6])
        ask = float(result["data"][1][10])
        print("bid: " + str(bid) + ", ask: " + str(ask))

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
    # items = TastyTradeApi.getFutureStreamerSymbols(apiUrl, authToken, ticker)

    await tt_dxfeed.subscribe([DXEvent.QUOTE], ["/MESU23:XCME"])

    await tt_dxfeed.listen(quote_callback)

    await tt_dxfeed.disconnect()

    closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

    if closeResult != 204:
        print("Unable to close/kill Tastytrade session.")


asyncio.run(main())
