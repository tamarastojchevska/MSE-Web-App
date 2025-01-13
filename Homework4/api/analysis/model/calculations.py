import numpy as np
import pandas as pd
from Homework4.api.analysis.model.technical_analysis import TechnicalAnalysis


class Calculations(TechnicalAnalysis):
    @staticmethod
    def get_trading_signals(val1, val2):
        if val1 > val2:
            return 1
        elif val1 < val2:
            return -1
        else:
            return 0

    @staticmethod
    def trading_signals_money_flow_index(high, low, close, mfi):
        buy_signal = []
        sell_signal = []

        for i in range(len(mfi)):
            if mfi[i] > high:
                buy_signal.append(np.nan)
                sell_signal.append(close[i])

            elif mfi < low:
                buy_signal.append(close[i])
                sell_signal.append(np.nan)

            else:
                sell_signal.append(np.nan)
                buy_signal.append(np.nan)

        return (buy_signal, sell_signal)

    @staticmethod
    def trading_signals_moving_average(short, long):
        signals = []
        for s, l in zip(short, long):
            signal = Calculations.get_trading_signals(s, l)
            signals.append(signal)
        return signals

    @staticmethod
    def simple_moving_average(price, days):
        return price.rolling(days).mean()

    @staticmethod
    def exponential_moving_average(price, days):
        return price.ewm(span=days).mean()

    @staticmethod
    def cumulative_moving_average(price):
        x = range(1, len(price) + 1)
        return np.cumsum(price) / np.array(x)

    @staticmethod
    def weighted_moving_average_trading_signals(price):
        w1 = [0.6, 0.25, 0.15, 0.05]
        second_list = list(range(10, 0, -1))
        w2 = second_list / np.sum(second_list)

        wma1 = price.rolling(len(w1)).apply(lambda x: (w1 * x).sum() / np.sum(w1), raw=True)
        wma2 = price.rolling(len(w2)).apply(lambda x: (w2 * x).sum() / np.sum(w2), raw=True)

        price.dropna(inplace=True)
        signal = []
        for w1, w2 in zip(wma1, wma2):
            signal.append(Calculations.get_trading_signals(w1, w2))

        return np.array(signal)

    @staticmethod
    def relative_strength_index(price):
        delta = price.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        average_gain = gain.rolling(window=14).mean()
        average_loss = loss.rolling(window=14).mean()

        rs = average_gain / average_loss.abs()
        return 100 - (100 / (1 + rs))

    @staticmethod
    def average_directional_index(high, low, close, lookback=14):
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

    @staticmethod
    def commodity_channel_index(high, low, close, period=40):
        TP = (high + low + close) / 3
        SMA = TP.rolling(period).mean()
        mad = TP.rolling(window=period).apply(
            lambda x: np.mean(np.abs(x - np.mean(x))), raw=True
        )
        CCI = (TP - SMA) / (0.015 * mad)
        return CCI

    @staticmethod
    def moving_average_convergence_divergence(price):
        ema1 = Calculations.exponential_moving_average(price, 1)
        ema30 = Calculations.exponential_moving_average(price, 30)
        return ema1 - ema30

    @staticmethod
    def money_flow_index(high, low, close, volume):
        typical_price = (high + low + close) / 3
        money_flow = typical_price * volume

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

        return 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

    @staticmethod
    def stochastic_oscillator(high, low, close, period=14):
        highs_max = np.maximum.accumulate(high)
        lows_min = np.minimum.accumulate(low)

        fast_k = 100 * ((close - lows_min) / (highs_max - lows_min))

        slow_k = np.zeros_like(fast_k)
        for i in range(period, len(fast_k)):
            slow_k[i] = np.mean(fast_k[i - period:i])

        return fast_k, slow_k
