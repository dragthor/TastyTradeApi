import requests
import json
import configparser


def readLocalConfig(fileName):
    config = configparser.ConfigParser()
    config.read(fileName)
    config.sections()

    email = config["DEFAULT"]["email"]
    password = config["DEFAULT"]["password"]
    apiUrl = config["DEFAULT"]["apiUrl"]

    return dict(email=email, password=password, apiUrl=apiUrl)


def getSessionAuthorizationToken(apiUrl, email, password):
    url = apiUrl + "/sessions"

    payload = {"login": email, "password": password}
    files = []
    headers = {}

    webResponse = requests.request(
        "POST", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["session-token"]


def validateSession(apiUrl, token):
    url = apiUrl + "/sessions/validate"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "POST", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["username"]


def closeSession(apiUrl, token):
    url = apiUrl + "/sessions"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "DELETE", url, headers=headers, data=payload, files=files
    )

    return webResponse.status_code  # 204 status code is success


def getCustomerAccounts(apiUrl, token):
    url = apiUrl + "/customers/me/accounts"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["items"]


def getAccountPositions(apiUrl, token, accountNumber):
    url = apiUrl + "/accounts/" + accountNumber + "/positions"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["items"]


def getAccountBalances(apiUrl, token, accountNumber):
    url = apiUrl + "/accounts/" + accountNumber + "/balances"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]


def getEquityOptionChains(apiUrl, token, ticker):
    url = apiUrl + "/option-chains/" + ticker + "/nested"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["items"]


def getFutureOptionChains(apiUrl, token, ticker):
    url = apiUrl + "/futures-option-chains/" + ticker + "/nested"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["option-chains"]


def getStreamerTokens(apiUrl, token):
    url = apiUrl + "/quote-streamer-tokens"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]


def getEquityStreamerSymbol(apiUrl, token, ticker):
    url = apiUrl + "/instruments/equities/" + ticker

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    return objJson["data"]["streamer-symbol"]


def getFutureStreamerSymbols(apiUrl, token, ticker):
    url = apiUrl + "/instruments/futures"

    payload = {}
    files = []
    headers = {"Authorization": token}

    webResponse = requests.request(
        "GET", url, headers=headers, data=payload, files=files
    )

    objJson = json.loads(webResponse.text)

    items = [p for p in objJson["data"]["items"] if p["product-code"] == ticker]

    return items
