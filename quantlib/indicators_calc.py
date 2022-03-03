# a calculator for indicators
# why separate out like this? why not directly replace inline?
# bc the modularity allows us to adjust for issues with talib
# we can re-implement if necessary without fuss

import talib
import numpy as np

def adx_series(high, low, close, n):
    return talib.ADX(high, low, close, timeperiod=n)

def ema_series(series, n):
    return talib.EMA(series, timeperiod=n)

def sma_series(series, n):
    return talib.SMA(series, timeperiod=n)

    # for instance this can be rewritten-
    # return pd.DataFrame(series).rolling(n).mean()

