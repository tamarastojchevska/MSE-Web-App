import numpy as np
import pandas as pd

def get_mfi(data):
    typical_price = (data['Price'] + data['Max'] + data['Min']) / 3
    money_flow = typical_price * data['Volume']

    period = 14
    positive_flow = []
    negative_flow = []

    for i in range(1, len(typical_price)):
        if typical_price[i] > typical_price[i - 1]:
            positive_flow.append(money_flow[i - 1])
            negative_flow.append(0)

        elif typical_price[i] < typical_price[i - 1]:
            negative_flow.append(money_flow[i - 1])
            positive_flow.append(0)

        else:
            positive_flow.append(0)
            negative_flow.append(0)

    positive_mf = []
    negative_mf = []

    for i in range(period - 1, len(positive_flow)):
        positive_mf.append(sum(positive_flow[i + 1 - period: i + 1]))

    for i in range(period - 1, len(negative_flow)):
        negative_mf.append(sum(negative_flow[i + 1 - period: i + 1]))

    return 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf) ))


def get_signal(data, high, low):
    buy_signal = []
    sell_signal = []

    for i in range(len(data['MFI'])):
        if data['MFI'][i] > high:
            buy_signal.append(np.nan)
            sell_signal.append(data['Price'][i])

        elif data['MFI'][i] < low:
            buy_signal.append(data['Price'][i])
            sell_signal.append(np.nan)

        else:
            sell_signal.append(np.nan)
            buy_signal.append(np.nan)

    return (buy_signal, sell_signal)

def parse_string_to_float(num):
    if num == ',':
        return 0.0
    else:
        return float(num.replace('.', '').replace(',', '.'))

def trading_signals(val1, val2):
    if val1 > val2:
        return 1
    elif val1 < val2:
        return -1
    else:
        return 0

def get_trading_signals_wma(data):
    w1 = [0.6, 0.25, 0.15, 0.05]
    second_list = list(range(10, 0, -1))
    w2 = second_list / np.sum(second_list)

    wma1 = data['Price'].rolling(len(w1)).apply(lambda x: (w1 * x).sum() / np.sum(w1), raw=True)
    wma2 = data['Price'].rolling(len(w2)).apply(lambda x: (w2 * x).sum() / np.sum(w2), raw=True)

    data.dropna(inplace=True)
    signal = []
    for w1, w2 in zip(wma1, wma2):
        signal.append(trading_signals(w1, w2))

    return np.array(signal)

def get_trading_signals(short, long):
    signals = []
    for s, l in zip(short, long):
        signal = trading_signals(s, l)
        signals.append(signal)
    return signals

def get_sma(data, days):
    return data.rolling(days).mean()

def get_ema(data, days):
    return data.ewm(span=days).mean()

def get_cma(data):
    x = range(1, len(data) + 1)
    return np.cumsum(data) / np.array(x)

def get_rsi(data):
    # Calculate rolling gains and losses
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate average gain and loss
    average_gain = gain.rolling(window=14).mean()
    average_loss = loss.rolling(window=14).mean()
    # Calculate RSI
    rs = average_gain / average_loss.abs()
    return 100 - (100 / (1 + rs))

def get_stochastic_oscillator(data, period=14):
    highs = data['Max']
    lows = data['Min']
    closes = data['Price']

    highs_max = np.maximum.accumulate(highs)
    lows_min = np.minimum.accumulate(lows)

    fast_k = 100 * ((closes - lows_min) / (highs_max - lows_min))

    slow_k = np.zeros_like(fast_k)
    for i in range(period, len(fast_k)):
        slow_k[i] = np.mean(fast_k[i - period:i])

    return fast_k, slow_k

def get_adx(high, low, close, lookback):
    plus_dm = high.diff()
    minus_dm = low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0

    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
    atr = tr.rolling(lookback).mean()

    plus_di = 100 * (plus_dm.ewm(alpha=1 / lookback).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha=1 / lookback).mean() / atr))
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
    adx_smooth = adx.ewm(alpha=1 / lookback).mean()
    return plus_di, minus_di, adx_smooth

def get_cci(df, period=40):
    TP = (df['Max']+df['Min']+df['Price'])/3
    SMA = TP.rolling(period).mean()
    mad = TP.rolling(window=period).apply(
        lambda x: np.mean(np.abs(x - np.mean(x))), raw=True
    )
    CCI = (TP - SMA) / (0.015 * mad)
    return CCI

def get_macd(data):
    ema1 = get_ema(data, 1)
    ema30 = get_ema(data, 30)
    return ema1 - ema30



