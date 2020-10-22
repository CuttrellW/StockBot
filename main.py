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
            cash = account.buying_power
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
                self.closePositions()
                time.sleep(310)



            # get the percent changes for each stock and designate top movers from the list
            self.getPercentChanges()
            self.stockList.sort(key=lambda x: x[1])

            topMovers = self.getTopMovers()

            if prevTopMovers:
                # find dropped members of top movers, and those whose percentage fell below zero
                for i in 0, len(prevTopMovers) - 1:
                    sell = False
                    if prevTopMovers[i][1] <= 0:
                        sell = True
                    else:
                        found = False
                        for j in 0, len(topMovers) - 1:
                            if prevTopMovers[i] == topMovers[j]:
                                found = True
                        if not found:
                            sell = True
                    if sell:
                        toSell.append(prevTopMovers[i])
                # find new members of Top Movers
                for i in 0, len(topMovers) - 1:
                    found = False
                    for j in 0, len(prevTopMovers) - 1:
                        if topMovers[i] == prevTopMovers[j]:
                            found = True
                    if not found:
                        toBuy.append(topMovers[i])



            # check to see if the top movers have changed

            # sell stocks if they drop out of top movers


            # execute buy orders for new top movers
            cashSplit = len(topMovers)


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
        length = int(len(self.stockList) / 4)
        for i in 0, length:
            topMovers.append(self.stockList[i])
        return topMovers
    # submit order
    def submitOrder(self, stock, qty, side):
        self.alpacaREST.submit_order(stock, qty, side, "market", "day")

    # close all positions
    def closePositions(self):
        positions = alpacaREST.list_positions()
        for p in positions:
            if p.qty > 0:
                try:
                    self.submitOrder(p.symbol, p.qty, "sell")
                    print("Successfully sold " + p.qty + " shares of " + p.symbol)
                except:
                    print("Failed to close order on " + p.qty + " shares of " + p.symbol)




run = StockBot()
run.main()
