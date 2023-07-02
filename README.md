# TastyTrade API Wrapper

For use as an automated trading bot for TastyTrade customers.

Referral link - https://start.tastytrade.com/#/login?referralCode=SP8DSHF682

## Warning

The code will actually place an order when `liveTradingEnabled` is True (default is False).

## Safety and Security

Never give your password to anyone.  This code is open source.  You can verify that the TastyTrade API Wrapper does not save nor transmit your password other than the initial authentication API call `getSessionAuthorizationToken`.  

All communication between TastyTrade and the TastyTrade API Wrapper is encrypted using SSL.

## Installation

`pip install tastyworks-aiocometd`
`pip install asyncio`
`pip install requests`

## Configuration

Your Tasty credentials and settings should be stored in a file named `tastytrade.ini`.  Modify, protect, and guard accordingly.

## Disclaimer

There is no implied warranty for any actions and results which arise from using it.  Any examples, rules, or algorithms are intended for educational purposes only and not financial advice.  Use at your own risk.