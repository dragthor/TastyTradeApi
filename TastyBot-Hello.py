import TastyTradeApi

email = "<YOUR_EMAIL>"
password = "<YOUR_PASSWORD>"
apiUrl = "https://api.tastyworks.com"
authToken = ""
userName = ""
liveTradingEnabled = False

authToken = TastyTradeApi.getSessionAuthorizationToken(apiUrl, email, password)

if len(authToken) == 0:
    print("Unable to get Tastytrade authorization token.")

userName = TastyTradeApi.validateSession(apiUrl, authToken)

if len(userName) == 0:
    print("Unable to validate Tastytrade session.")

accounts = TastyTradeApi.getCustomerAccounts(apiUrl, authToken)

primaryAccount = accounts[0]["account"]["account-number"]

balances = TastyTradeApi.getAccountBalances(apiUrl, authToken, primaryAccount)

positions = TastyTradeApi.getAccountPositions(apiUrl, authToken, primaryAccount)

print(
    "----------------------------------------------------------------------------------------"
)
print(
    "Account: "
    + primaryAccount
    + ", Cash: "
    + balances["cash-balance"]
    + ", Reg-T Margin: "
    + balances["reg-t-margin-requirement"]
    + ", Futures Margin: "
    + balances["futures-margin-requirement"]
)
print(
    "----------------------------------------------------------------------------------------"
)

positions.sort(key=lambda x: x["underlying-symbol"])

for position in positions:
    print(
        position["underlying-symbol"]
        + " "
        + str(position["quantity"])
        + " "
        + position["symbol"]
        + " "
        + position["quantity-direction"]
        + " "
        + str(position["expires-at"])
    )

closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

if closeResult != 204:
    print("Unable to close/kill Tastytrade session.")
