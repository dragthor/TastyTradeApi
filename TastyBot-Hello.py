import TastyTradeApi
from datetime import datetime

authToken = ""
userName = ""
liveTradingEnabled = False

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

accounts = TastyTradeApi.getCustomerAccounts(apiUrl, authToken)

primaryAccount = accounts[0]["account"]["account-number"]

balances = TastyTradeApi.getAccountBalances(apiUrl, authToken, primaryAccount)

positions = TastyTradeApi.getAccountPositions(apiUrl, authToken, primaryAccount)

cash = float(balances["cash-balance"])
regTMargin = float(balances["reg-t-margin-requirement"])
spanMargin = float(balances["futures-margin-requirement"])
buyPower = round(((regTMargin + spanMargin) / cash) * 100, 2)

print(
    "------------------------------------------------------------------------------------------------------"
)
print(
    "Account: "
    + primaryAccount
    + ", Cash: "
    + str(cash)
    + ", Reg-T Margin: "
    + str(regTMargin)
    + ", Futures Margin: "
    + str(spanMargin)
    + ", Buying Power: " + str(buyPower) + "%"
)
print(
    "------------------------------------------------------------------------------------------------------"
)

positions.sort(key=lambda x: x["underlying-symbol"])

for position in positions:
    # 2023-08-17T18:30:00.000+00:00
    expiration = datetime.strptime(position["expires-at"], '%Y-%m-%dT%H:%M:%S.%f+00:00') 
    today =  datetime.today()
    dte = abs((today - expiration).days)

    print(
        position["underlying-symbol"]
        + "\t"
        + str(position["quantity"])
        + "\t"
        + position["symbol"]
        + "\t"
        + position["quantity-direction"]
        + "\t"
        + str(position["expires-at"])
        + "\t"
        + str(dte)
    )

closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

if closeResult != 204:
    print("Unable to close/kill Tastytrade session.")
