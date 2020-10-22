import alpaca_trade_api as tradeapi

keyId = 'PK1U4U5S4YAAKJD094M6'
secretKey = 'jdLw3EiiBsNfGfkUiaM6laBhLPmMndVXxwdOPl3M'
paperBaseURL = 'https://paper-api.alpaca.markets'

alpacaREST = tradeapi.REST(keyId, secretKey, paperBaseURL, 'v2')