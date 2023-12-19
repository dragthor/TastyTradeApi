import TastyTradeApi as tasty
import asyncio
import time

from DXFeed import *

listen_loop_seconds = 60

# https://symbol-lookup.dxfeed.com/

# tickers = [ ".SPY240216P400", ".SPY240216C500" ]

tickers = [ ".SPX240216P4000", ".SPX240216C5000" ]


liveTradingEnabled = False


async def main():
    email = ""
    password = ""
    apiUrl = ""
    authToken = ""
    userName = ""

    async def quote_callback(result):
        t = result["data"][0]

        if t == "Quote":
            for i in range(len(result["data"])):
                try:
                    if (i == 0):
                        continue

                    ticker = result["data"][i][0]
                    bid = float(result["data"][i][6]) # bidPrice
                    ask = float(result["data"][i][10]) # askPrice
                    
                    print(ticker + " - mid: " + str(midpoint(bid, ask)) + ", bid: " + str(bid) + ", ask: " + str(ask))
                except:
                    print("error looping over quotes results data")

        elif t == "Greeks":
            try:
                j = 1
                ticker = result["data"][j][0]
                volatility = float(result["data"][j][7]) # volatility 
                delta = float(result["data"][j][8]) # delta
                theta = float(result["data"][j][10]) # theta
                vega = float(result["data"][j][12]) # vega
                gamma = float(result["data"][j][9]) # gamma
                rho = float(result["data"][j][11]) # rho

                print(ticker + " - d: " + str(delta) + " t: " + str(theta) + " v: " + str(vega) + " g: " + str(gamma) + " r: " + str(rho) + " iv: " + str(volatility))
            except:
                print("error looping over greeks results data")

    def midpoint(bid, ask):
        return round((bid + (ask - bid) / 2), 2)

    settings = tasty.readLocalConfig("tastytrade.ini")
    email = settings["email"]
    password = settings["password"]
    apiUrl = settings["apiUrl"]

    authToken = tasty.getSessionAuthorizationToken(apiUrl, email, password)

    if len(authToken) == 0:
        print("Unable to get Tastytrade authorization token.")

    userName = tasty.validateSession(apiUrl, authToken)

    if len(userName) == 0:
        print("Unable to validate Tastytrade session.")

    streamerTokens = tasty.getStreamerTokens(apiUrl, authToken)

    dxFeedToken = streamerTokens["token"]
    streamerUrl = streamerTokens["streamer-url"]
    websocketUrl = streamerTokens["websocket-url"] + "/cometd"

    tt_dxfeed = DXFeed(websocketUrl, dxFeedToken)

    await tt_dxfeed.connect()

    await tt_dxfeed.subscribe([DXEvent.QUOTE, DXEvent.GREEKS], tickers)

    t_end = time.time() + listen_loop_seconds
    
    while time.time() < t_end:
        await tt_dxfeed.listen(quote_callback)

    await tt_dxfeed.disconnect()

    closeResult = tasty.closeSession(apiUrl, authToken)

    if closeResult != 204:
        print("Unable to close/kill Tastytrade session.")


asyncio.run(main())
