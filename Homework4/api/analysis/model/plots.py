import json
import pandas as pd
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Homework4.api.analysis.model.technical_analysis import TechnicalAnalysis


class Plots(TechnicalAnalysis):
    height = 500
    width = 1000

    @staticmethod
    def chart_trading_signals(buy_signals, sell_signals, hold_signals, fig, col, row):
        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals['Price'],
            mode='markers',
            marker_symbol='triangle-up',
            marker_size=10,
            marker_color='rgb(0, 255, 0)',
            text='Buy',
            name='Buy'
        ), col=col, row=row)

        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals['Price'],
            mode='markers',
            marker_symbol='triangle-down',
            marker_size=10,
            marker_color='rgb(255, 0, 0)',
            text='Sell',
            name='Sell'
        ), col=col, row=row)

        fig.add_trace(go.Scatter(
            x=hold_signals.index,
            y=hold_signals['Price'],
            mode='markers',
            marker_symbol='square',
            marker_size=10,
            marker_color='rgb(0, 0, 255)',
            text='Hold',
            name='Hold'
        ), col=col, row=row)

    @staticmethod
    def simple_moving_average(data, sma_short, sma_medium, sma_long, signals):
        data['SMA-short'] = sma_short
        data['SMA-medium'] = sma_medium
        data['SMA-long'] = sma_long

        data['Signal'] = signals

        fig = px.line(data, x=data.index, y=['Price', 'SMA-short', 'SMA-medium', 'SMA-long'])
        Plots.chart_trading_signals(data[data['Signal'] == 1],
                              data[data['Signal'] == -1],
                              data[data['Signal'] == 0],
                              fig, 1, 1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Simple Moving Average")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def exponential_moving_average(data, ema_short, ema_medium, ema_long, signals):
        data['EMA-short'] = ema_short
        data['EMA-medium'] = ema_medium
        data['EMA-long'] = ema_long

        data['Signal'] = signals

        fig = px.line(data, x=data.index, y=['Price', 'EMA-short', 'EMA-medium', 'EMA-long'])
        Plots.chart_trading_signals(data[data['Signal'] == 1],
                              data[data['Signal'] == -1],
                              data[data['Signal'] == 0],
                              fig, 1, 1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Exponential Moving Average")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def cumulative_moving_average(data, cma):
        data['CMA'] = cma
        fig = px.line(data, x=data.index, y=['Price', 'CMA'])
        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Cumulative Moving Average")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def weighted_moving_average(data, signals):
        data['Signal'] = signals

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Line(x=data.index, y=data, line=dict(color='black'), name='Price'))
        Plots.chart_trading_signals(data[data['Signal'] == 1],
                              data[data['Signal'] == -1],
                              data[data['Signal'] == 0],
                              fig, 1, 1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Weighted Moving Average")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def moving_average_convergence_divergence(data, macd, ema_medium):
        data['MACD'] = macd

        # signal line
        data['Signal line'] = ema_medium

        fig = px.line(data, x=data.index, y=['Price', 'MACD', 'Signal line'])

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Moving Average Convergence Divergence")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def ribbon_moving_averages(data, sma_medium, ema_medium, cma, macd):
        data['SMA'] = sma_medium
        data['EMA'] = ema_medium
        data['CMA'] = cma
        data['MACD'] = macd
        fig = px.line(data, x=data.index, y=['Price', 'SMA', 'EMA', 'CMA', 'MACD'])

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Ribbon Moving Averages")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def relative_strength_index(data, rsi):
        data['RSI'] = rsi

        fig = make_subplots(rows=2, cols=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data,
            name='Price',
        ), row=1, col=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data['RSI'],
            name='RSI'
        ), row=2, col=1)

        fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)
        fig.add_hline(y=70, line=dict(color='green', dash='dash'), row=2, col=1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Relative Strength Index (RSI)")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    @staticmethod
    def average_directional_index(data, adx):
        data['plus_di'] = pd.DataFrame(adx[0]).rename(columns={0: 'plus_di'})
        data['minus_di'] = pd.DataFrame(adx[1]).rename(columns={0: 'minus_di'})
        data['adx'] = pd.DataFrame(adx[2]).rename(columns={0: 'adx'})

        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Line(
            x=data.index,
            y=data['Price'],
            name='Price'
        ), row=1, col=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data['adx'],
            name='ADX',
            line=dict(color='blue')
        ), row=2, col=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data['plus_di'],
            name='plus_di',
            line=dict(color='green'),
            opacity=0.5
        ), row=2, col=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data['minus_di'],
            name='minus_di',
            line=dict(color='red'),
            opacity=0.5
        ), row=2, col=1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Average Directional Index (ADX)")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def commodity_channel_index(data, cci):
        data['cci'] = cci
        fig = px.line(data, x=data.index, y=['Price', 'cci'])

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Commodity Channel Index (CCI)")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def money_flow_index(data, mfi, signals):
        new_df = data[14:]
        new_df['MFI'] = mfi
        new_df['Buy'] = signals[0]
        new_df['Sell'] = signals[1]
        new_df['Price'] = data['Price']

        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Line(
            x=new_df.index,
            y=new_df['Price'],
            name='Price'
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=new_df['Buy'].index,
            y=new_df['Buy'],
            mode='markers',
            marker_symbol='triangle-up',
            marker_size=10,
            marker_color='rgb(0, 255, 0)',
            text='Buy',
            name='Buy'
        ), col=1, row=1)

        fig.add_trace(go.Scatter(
            x=new_df['Sell'].index,
            y=new_df['Sell'],
            mode='markers',
            marker_symbol='triangle-down',
            marker_size=10,
            marker_color='rgb(255, 0, 0)',
            text='Sell',
            name='Sell'
        ), col=1, row=1)

        fig.add_trace(go.Line(
            x=new_df.index,
            y=new_df['MFI'],
            name='MFI',
        ), row=2, col=1)

        fig.add_hline(y=10, line=dict(color='orange', dash='dash'), row=2, col=1)
        fig.add_hline(y=20, line=dict(color='blue', dash='dash'), row=2, col=1)
        fig.add_hline(y=80, line=dict(color='blue', dash='dash'), row=2, col=1)
        fig.add_hline(y=90, line=dict(color='orange', dash='dash'), row=2, col=1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Money Flow Index (MFI)")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @staticmethod
    def stochastic_oscillator(data, stochastic, sma_50, sma_200):
        data['fast_k'], data['slow_k'] = stochastic

        data['ma50'] = sma_50
        data['ma200'] = sma_200

        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(go.Line(
            x=data.index,
            y=data['Price'],
            name='Price'
        ), row=1, col=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data['ma50'],
            name='MA50'
        ), row=1, col=1)
        fig.add_trace(go.Line(
            x=data.index,
            y=data['ma200'],
            name='MA200'
        ), row=1, col=1)

        fig.add_trace(go.Line(
            x=data.index,
            y=data['fast_k'],
            name='fast_k'
        ), row=2, col=1)
        fig.add_trace(go.Line(
            x=data.index,
            y=data['slow_k'],
            name='slow_k'
        ), row=2, col=1)

        fig.add_hline(y=20, line=dict(color='red', dash='dash'), row=2, col=1)
        fig.add_hline(y=80, line=dict(color='blue', dash='dash'), row=2, col=1)

        fig.update_layout(height=Plots.height, width=Plots.width, title_text="Stochastic Oscillator")

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)