import backtrader as bt
import ccxt
import pandas as pd
from ta.volatility import BollingerBands, AverageTrueRange
import schedule
import datetime
import time
import bot
pd.set_option("display.max_rows", None, "display.max_columns", None)


class MyStrategy(bt.Strategy):

    def __init__(self):
        print("init")
        self.count=0
        self.data=bot.in_uptrend
    def next(self):
        current = self.count
        previous = self.count-1
        print(str(previous)+" "+str(current))
        print("in Position:"+str(self.position))

        if(current==0):
            print('this first bar,do not anything')
        else:
            if not self.data[previous] and self.data[current]:
                if not self.position:
                    print('buy')
                    self.order=self.buy()
                    # self.position=True
                else:
                    print("you are already in position")
            elif self.data[previous] and not self.data[current]:
                if self.position:
                    print('sell!')
                    self.order=self.sell()
                    # self.position=False
                else:
                    print("you are not in a position")
            else:
                print('We are between bands!')
        self.count = self.count + 1
