import ccxt
import ta.volatility
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

def supertrend(df, period=14, atr_multiplier=3):
    bb_indacator = ta.volatility.BollingerBands(df['close'], 20)
    df['upperband'] = bb_indacator.bollinger_hband()
    df['lowerband'] = bb_indacator.bollinger_lband()
    atr = ta.volatility.average_true_range(df['high'], df['low'], df['close'])
    df['atr']=atr
    df['in_uptrend'] = None
    for current in range(1, len(df.index)):
        previous = current - 1
        if (df['close'][current] > df['upperband'][previous]):
            # UP TREND
            df['in_uptrend'][current] = True
        elif (df['close'][current] < df['lowerband'][previous]):
            # down trend
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if (df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]):
                df['lowerband'][current] = df['lowerband'][previous]
            elif (not (df['in_uptrend'][current]) and df['upperband'][current] > df['upperband'][previous]):
                df['lowerband'][current] = df['lowerband'][previous]
    return df


def check(data):
    print(data.tail(2))
    current = len(data) - 1
    previous = len(data) - 2
    if not data['in_uptrend'][previous] and data['in_uptrend'][current]:
        print('buy')
    elif data['in_uptrend'][previous] and not data['in_uptrend'][current]:
        print('sell!')
    else:
        print('wait!')


#
binance = ccxt.binance()
bars = binance.fetch_ohlcv('ETH/USDT', timeframe='1h', limit=365)
data = pd.DataFrame(bars[:-1], columns=['time', 'open', 'high', 'low', 'close', 'volume'])
newdata=supertrend(data)
in_uptrend=newdata['in_uptrend']
f=open('datatoread','w')
f.write(newdata.to_string())
f.close()
# def run_bot():
#     write = newdata
#     # for index,row in newdata.iterrows():
#     #  print(str(index)+' '+str(row['timestamp'])+' '+str(row['in_uptrend']))
#     check(newdata)
