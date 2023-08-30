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
netLiquidity = float(balances["net-liquidating-value"])
regTMargin = float(balances["reg-t-margin-requirement"])
spanMargin = float(balances["futures-margin-requirement"])
totalMargin = regTMargin + spanMargin;
buyPower = round((totalMargin / cash) * 100, 2)

print(
    "------------------------------------------------------------------------------------------------------"
)
print(
    "Cash: "
    + str(cash)
    + ", Net Liq: "
    + str(netLiquidity)
    + ", Reg-T: "
    + str(regTMargin)
    + ", Futures: "
    + str(spanMargin)
    + ", Margin: "
    + str(totalMargin)
    + ", BP: " + str(buyPower) + "%"
)
print(
    "------------------------------------------------------------------------------------------------------"
)

positions.sort(key=lambda x: (x["expires-at"], x["underlying-symbol"], x["symbol"]))

for position in positions:
    # 2023-08-17T18:30:00.000+00:00
    expiration = datetime.strptime(position["expires-at"], '%Y-%m-%dT%H:%M:%S.%f+00:00') 
    today =  datetime.today()
    dte = abs((today - expiration).days) - 1

    print(
        position["underlying-symbol"]
        + "\t"
        + str(position["quantity"])
        + "\t"
        + position["symbol"]
        + "\t"
        + position["quantity-direction"]
        + "\t"
        + str(dte)
    )

closeResult = TastyTradeApi.closeSession(apiUrl, authToken)

if closeResult != 204:
    print("Unable to close/kill Tastytrade session.")
