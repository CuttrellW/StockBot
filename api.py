import alpaca_trade_api as tradeapi

keyId = 'PKIE65M409RNDZP8AYU0'
secretKey = 'LvWzKDmZGh2uzOUQgxU8NGj3uGo4RtoiFq44c4Uf'
paperBaseURL = 'https://paper-api.alpaca.markets'

alpacaREST = tradeapi.REST(keyId, secretKey, paperBaseURL, 'v2')