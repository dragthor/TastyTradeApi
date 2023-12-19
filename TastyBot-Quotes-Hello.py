import TastyTradeApi
import asyncio
import time

from DXFeed import *

# https://symbol-lookup.dxfeed.com/

#tickers = [ ".SPY240119P420", ".SPY240216P420" ]

tickers = [ ".SPX240119P4200", ".SPX240216P4200" ]


liveTradingEnabled = False


async def main():
    email = ""
    password = ""
    apiUrl = ""
    authToken = ""
    userName = ""

    async def quote_callback(result):
        t = result["data"][0][0]
        ticker = result["data"][1][0]

        if t == "Quote":    
            bid = float(result["data"][1][6]) # bidPrice
            ask = float(result["data"][1][10]) # askPrice
            print(ticker + " - mid: " + str(midpoint(bid, ask)) + ", bid: " + str(bid) + ", ask: " + str(ask))
                
        if t == "Greeks":
            volatility = float(result["data"][1][7]) # volatility 
            delta = float(result["data"][1][8]) # delta
            theta = float(result["data"][1][10]) # theta
            vega = float(result["data"][1][12]) # vega
            gamma = float(result["data"][1][9]) # gamma
            rho = float(result["data"][1][11]) # rho

            print(ticker + " - d: " + str(delta) + " t: " + str(theta) + " v: " + str(vega) + " g: " + str(gamma) + " r: " + str(rho) + " iv: " + str(volatility))
        
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
    # items = TastyTradeApi.getEquityStreamerSymbol(apiUrl, authToken, tickers[0])

    #print(items)

    await tt_dxfeed.subscribe([DXEvent.QUOTE, DXEvent.GREEKS], tickers)

    seconds = 10
    t_end = time.time() + seconds
    
    while time.time() < t_end:
        await tt_dxfeed.listen(quote_callback)

    await tt_dxfeed.disconnect()

    closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

    if closeResult != 204:
        print("Unable to close/kill Tastytrade session.")


asyncio.run(main())
