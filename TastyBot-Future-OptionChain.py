import TastyTradeApi

email = "<YOUR_EMAIL>"
password = "<YOUR_PASSWORD>"
apiUrl = "https://api.tastyworks.com"
ticker = "MES"
authToken = ""
userName = ""
liveTradingEnabled = False
exitTastyBot = False

authToken = TastyTradeApi.getSessionAuthorizationToken(apiUrl, email, password)

if len(authToken) == 0:
    print("Unable to get Tastytrade authorization token.")

userName = TastyTradeApi.validateSession(apiUrl, authToken)

if len(userName) == 0:
    print("Unable to validate Tastytrade session.")

if exitTastyBot == False:
    optionChains = TastyTradeApi.getFutureOptionChains(apiUrl, authToken, ticker)

    # Find expiration between 40 and 60 days.
    for chain in optionChains:
        expirations = chain["expirations"]
        for expiry in expirations:
            dte = expiry["days-to-expiration"]
            if dte > 40 and dte < 60:
                print(dte)
                desiredExpiration = expiry
                break

    for strike in desiredExpiration["strikes"]:
        print(strike)

streamerSymbols = TastyTradeApi.getFutureStreamerSymbols(apiUrl, authToken, ticker)

print(streamerSymbols)

closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

if closeResult != 204:
    print("Unable to close/kill Tastytrade session.")
