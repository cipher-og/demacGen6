from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.trend import SMAIndicator


def __macd_stra_(df, fast_period=3, slow_period=10, signal_period=16):
    dataframe = df[-25:]
    __macd_ = MACD(dataframe, window_slow=slow_period, window_fast=fast_period, window_sign=signal_period)

    _macd_nw_ = __macd_.macd()[-1:]
    _macd_pre_ = __macd_.macd()[-2:-1]
    _macd_sin_nw_ = __macd_.macd_signal()[-1:]
    _macd_sin_pre_ = __macd_.macd_signal()[-2:-1]

    if (_macd_nw_ > _macd_sin_nw_) and \
            (_macd_pre_ < _macd_sin_pre_):
        return True

    elif (_macd_nw_ < _macd_sin_nw_) and \
            (_macd_pre_ > _macd_sin_pre_):
        return False
    else:
        return None


def __rsi_pullback_(df, sma_period=200, rsi_period=10):
    dataframe = df[-200:]
    _rsi_entry_value = 30
    _rsi_exit_value = 40
    __sma_ = SMAIndicator(dataframe, 200)
    __rsi_ = RSIIndicator(dataframe, 10)
    __sma_ = __sma_.sma_indicator()[-1:]
    __rsi_ = __rsi_.rsi()[-1:]
    __last_close = float(dataframe[-1:])
    if ((__last_close > __sma_) * (__rsi_ < _rsi_entry_value)).bool():
        return True

    elif (__rsi_ > _rsi_exit_value).bool():
        return False

    else:
        '''empty'''


def __is_consolidating(df, consolidate_per=2):
    __resent_closes_1_ = df[-15:]

    __max_close = float(__resent_closes_1_.max())
    __min_close = float(__resent_closes_1_.min())
    threshold = 1 - (consolidate_per / 100)

    if __min_close > (__max_close * threshold):
        return True

    else:
        return False


def __breakout_(df):
    __last_close = df[-1:].values[0:]

    if __is_consolidating(df=df[:-1]):
        __resent_closes_2_ = df[-16:-1]

        if __last_close > __resent_closes_2_.max():
            return True

    else:
        return False
