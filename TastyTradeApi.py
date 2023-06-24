import requests
import json


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
