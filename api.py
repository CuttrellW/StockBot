import alpaca_trade_api as tradeapi

keyId = #insert key id
secretKey = #insert secret key
paperBaseURL = 'https://paper-api.alpaca.markets'

alpacaREST = tradeapi.REST(keyId, secretKey, paperBaseURL, 'v2')