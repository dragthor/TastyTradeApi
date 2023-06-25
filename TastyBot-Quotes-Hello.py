import TastyTradeApi

email = "<YOUR_EMAIL>"
password = "<YOUR_PASSWORD>"
apiUrl = "https://api.tastyworks.com"
ticker = "SPY"
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

streamerTokens = TastyTradeApi.getStreamerTokens(apiUrl, authToken)

dxFeedToken = streamerTokens["token"]
streamerUrl = streamerTokens["streamer-url"]
websocketUrl = streamerTokens["websocket-url"]

print(dxFeedToken)

closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

if closeResult != 204:
    print("Unable to close/kill Tastytrade session.")