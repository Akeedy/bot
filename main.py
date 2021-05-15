# This is a sample Python script.

import datetime
import ccxt
import backtrader as bt
from supertrend_strategy import MyStrategy
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def fetch_data(exchange, symbol):
    bars = exchange.fetch_ohlcv(symbol=symbol, timeframe='1h', limit=365)
    f = open('data.csv', 'w')
    for i in bars:
        i[0] = datetime.datetime.utcfromtimestamp(i[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        text = str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "," + str(i[4]) + ',' + str(
            i[5]) + '\n'
        f.write(text)
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    binance = ccxt.binance()
    fetch_data(binance, 'ETH/USDT')

    data = bt.feeds.GenericCSVData(
        dataname='data.csv',
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1
    )

    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.addstrategy(MyStrategy)
    print('starting portfolio value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
