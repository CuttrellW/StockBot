from api import alpacaREST
import pandas as pd
import datetime
import time
from fleet import fleet


class StockBot:
    def __init__(self):
        self.alpacaREST = alpacaREST
        self.stockList = []
        for stock in fleet:
            self.stockList.append([stock, 0])


    def main(self):
        # close all open orders
        openOrders = alpacaREST.list_orders(status="open")
        for order in openOrders:
            alpacaREST.cancel_order(order.id)
        # check to see if market is open
        print("Checking market is open...")
        marketOpen = alpacaREST.get_clock().is_open
        while not marketOpen:
            clock = alpacaREST.get_clock()
            openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
            currentTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeToOpen = int((openingTime - currentTime) / 60)
            if timeToOpen > 2:

                print("Market closed. Please wait " + str(timeToOpen) + " minutes until open.")
                time.sleep(60)
            else:
                print("Market opening soon, getting ready...")
                time.sleep(10)
            marketOpen = alpacaREST.get_clock().is_open

        print("Market open. Beginning operation!")

        prevTopMovers = []
        while True:
            account = alpacaREST.get_account()
            cash = int(float(account.buying_power))
            positions = alpacaREST.list_positions()
            toSell = []
            toBuy = []

            # check if market is closing soon

            clock = alpacaREST.get_clock()
            closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
            currentTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeUntilClose = closingTime - currentTime
            if timeUntilClose < 5:
                print("Market about to close. Selling all positions.")
                for order in openOrders:
                    alpacaREST.cancel_order(order.id)
                self.closePositions(positions)
                time.sleep(310)



            # get the percent changes for each stock and designate top movers from the list
            self.getPercentChanges()
            self.stockList.sort(key=lambda x: x[1], reverse=True)

            topMovers = self.getTopMovers()

            if prevTopMovers:
                # find dropped members of top movers, and those whose percentage fell below zero
                for i in range(len(prevTopMovers)):
                    sell = False
                    if prevTopMovers[i][1] <= 0 and self.heldPosition(prevTopMovers[i][0]):
                        sell = True
                    else:
                        found = False
                        for j in range(len(topMovers)):
                            if prevTopMovers[i] == topMovers[j]:
                                found = True
                        if not found:
                            sell = True
                    if sell:
                        toSell.append(prevTopMovers[i])
                # find new members of Top Movers
                for i in range(len(topMovers)):
                    found = False
                    for j in range(len(prevTopMovers)):
                        if topMovers[i] == prevTopMovers[j]:
                            found = True
                    if not found and topMovers[i][1] > 0:
                        toBuy.append(topMovers[i])
            else:
                for i in range(len(topMovers)):
                    if topMovers[i][1] > 0:
                        toBuy.append(topMovers[i])

            # send sell orders
            if toSell:
                for stock in toSell:
                    symbol = stock[0]
                    qty = self.getQuantity(symbol)
                    #print("Submitting order to sell " + str(qty) + " shares of " + str(symbol))
                    self.submitOrder(symbol, qty, "sell")

            if toBuy:
                cashSplit = int(cash / len(toBuy) * 0.95)
                for stock in toBuy:
                    symbol = stock[0]
                    quote = alpacaREST.get_last_quote(symbol)
                    price = quote.askprice
                    qty = int(cashSplit / price)
                    #print("Submitting order to buy " + str(qty) + " shares of " + str(symbol))
                    self.submitOrder(symbol, qty, "buy")



            prevTopMovers = topMovers
            print(self.stockList)
            print(topMovers)
            time.sleep(3)
    # check if market is closing soon

    # get percent changes
    def getPercentChanges(self):
        length = 10
        for stock in self.stockList:

            barset = alpacaREST.get_barset(stock[0], 'minute', limit=1)
            stockBars = barset[stock[0]]
            minuteOpen = stockBars[0].o
            minuteClose = stockBars[-1].c
            percentChange = (minuteOpen - minuteClose) / minuteOpen * 100
            stock[1] = percentChange


    # designate top movers
    def getTopMovers(self):
        topMovers = []
        length = int(len(self.stockList) / 3)
        if length == 0:
            topMovers.append(self.stockList[0])
        else:
            for i in range(length):
                topMovers.append(self.stockList[i])
        return topMovers
    # submit order
    def submitOrder(self, stock, qty, side):
        try:
            self.alpacaREST.submit_order(stock, qty, side, "market", "day")
            print("Successful " + str(side) + " of " + str(qty) + " shares of " + str(stock))
        except:
            print("Failed to " + str(side) + " " + str(qty) + " shares of " + str(stock))

    # close all positions
    def closePositions(self, positions):
        for p in positions:
            if p.qty > 0:
                try:
                    self.submitOrder(p.symbol, p.qty, "sell")
                except:
                    print("ORDER NOT CLOSED")


    def heldPosition(self, stock):
        found = False
        positions = alpacaREST.list_positions()
        for p in positions:
            if stock == p.symbol:
                found = True
        return found

    def getQuantity(self, stock):
        positions = alpacaREST.list_positions()
        for p in positions:
            if stock == p.symbol:
                return int(p.qty)

run = StockBot()
run.main()
