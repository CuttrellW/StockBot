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
            print("Market closed. Please wait " + str(timeToOpen) + " minutes until open.")
            time.sleep(60)
            marketOpen = alpacaREST.get_clock().is_open

        print("Market open. Beginning operation!")

        while True:
            # check if market is closing soon

            clock = alpacaREST.get_clock()
            closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
            currentTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeUntilClose = closingTime - currentTime



            # get the percent changes for each stock and designate top movers from the list
            self.getPercentChanges()

            # sell stocks if they drop out of top movers

            # execute buy orders for new top movers

    # check if market is closing soon

    # get percent changes
    def getPercentChanges(self):
        length = 10
        for i, stock in enumerate(self.stockList):



run = StockBot()
run.main()
