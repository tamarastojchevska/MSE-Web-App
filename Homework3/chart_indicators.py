import json
import sqlite3
import pandas as pd
from datetime import *
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Homework3.indicators_calculations import *


def get_data(from_date, to_date, table_name):
    file = 'database.db'

    if from_date == '':
        from_date = date.today() - timedelta(days=3650)
        from_date = from_date.strftime('%Y-%m-%d')
    if to_date == '':
        to_date = date.today().strftime('%Y-%m-%d')

    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("SELECT * from %s WHERE DateFormated > ? AND DateFormated < ?" % table_name, [from_date, to_date])

    data = cursor.fetchall()
    data = pd.DataFrame(data=data,
                        columns=['Date',
                                 'Price',
                                 'Max',
                                 'Min',
                                 'AvgPrice',
                                 'chg',
                                 'Volume',
                                 'TurnoverBEST',
                                 'Turnover',
                                 'DateFormated'])

    data.sort_values('DateFormated', inplace=True, ascending=True)
    data.set_index('DateFormated', inplace=True)

    data['Price'] = data['Price'].apply(lambda x: parse_string_to_float(x))
    data['Max'] = data['Max'].apply(lambda x: parse_string_to_float(x))
    data['Min'] = data['Min'].apply(lambda x: parse_string_to_float(x))
    if data.dtypes['Volume'] == 'int64' or data.dtypes['Volume'] == 'int32':
        data['Volume'] = data['Volume'].astype('float64')
    else:
        data['Volume'] = data['Volume'].apply(lambda x: x.replace(',', '')).astype('float')

    data = data.filter(['Price', 'Max', 'Min', 'Volume'])
    return data


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


def simple_moving_average(data):
    data['SMA-short'] = get_sma(data['Price'], 1)
    data['SMA-medium'] = get_sma(data['Price'], 7)
    data['SMA-long'] = get_sma(data['Price'], 30)

    data['Signal'] = get_trading_signals(data['SMA-short'], data['SMA-long'])

    fig = px.line(data, x=data.index, y=['Price', 'SMA-short', 'SMA-medium', 'SMA-long'], height=600)
    chart_trading_signals(data[data['Signal'] == 1],
                          data[data['Signal'] == -1],
                          data[data['Signal'] == 0],
                          fig, 1, 1)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def exponential_moving_average( data):
    data['EMA-short'] = get_ema(data['Price'], 1)
    data['EMA-medium'] = get_ema(data['Price'], 7)
    data['EMA-long'] = get_ema(data['Price'], 30)

    data['Signal'] = get_trading_signals(data['EMA-short'], data['EMA-long'])

    fig = px.line(data, x=data.index, y=['Price', 'EMA-short', 'EMA-medium', 'EMA-long'])
    chart_trading_signals(data[data['Signal'] == 1],
                          data[data['Signal'] == -1],
                          data[data['Signal'] == 0],
                          fig, 1, 1)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def cumulative_moving_average(data):
    data['CMA'] = get_cma(data['Price'])
    fig = px.line(data, x=data.index, y=['Price', 'CMA'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def weighted_moving_average(data):
    data['Signal'] = get_trading_signals_wma(data)

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Line(x=data.index, y=data['Price'], line=dict(color='black'), name='Price'))
    chart_trading_signals(data[data['Signal'] == 1],
                          data[data['Signal'] == -1],
                          data[data['Signal'] == 0],
                          fig, 1, 1)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def ribbon_moving_averages(data):
    data['SMA'] = get_sma(data['Price'], 7)
    data['EMA'] = get_ema(data['Price'], 7)
    data['CMA'] = get_cma(data['Price'])
    data['MACD'] = get_macd(data['Price'])
    fig = px.line(data, x=data.index, y=['Price', 'SMA', 'EMA', 'CMA', 'MACD'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def macd(data):

    data['MACD'] = get_macd(data['Price'])

    # signal line
    data['Signal line'] = get_ema(data['MACD'], 7)

    fig = px.line(data, x=data.index, y=['Price', 'MACD', 'Signal line'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def rsi(data):

    data['RSI'] = get_rsi(data['Price'])

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(go.Line(
        x=data.index,
        y=data['Price'],
        name='Price',
    ), row=1, col=1)

    fig.add_trace(go.Line(
        x=data.index,
        y=data['RSI'],
        name='RSI'
    ), row=2, col=1)

    fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)
    fig.add_hline(y=70, line=dict(color='green', dash='dash'), row=2, col=1)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def stochastic_oscillator(data):
    data['fast_k'], data['slow_k'] = get_stochastic_oscillator(data, period=14)

    data['ma50'] = get_sma(data['Price'], 50)
    data['ma200'] = get_sma(data['Price'], 200)

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

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def adx_indicator(data):
    data['adx'] = get_adx(data)

    fig = px.line(data, x=data.index, y=['Price', 'adx'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def chart_cci(data):
    data['cci'] = get_cci(data)
    fig = px.line(data, x=data.index, y=['Price', 'cci'])
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def money_fow_index(data):
    new_df = data[14:]
    new_df['MFI'] = get_mfi(data)
    new_df['Buy'] = get_signal(new_df, 80, 20)[0]
    new_df['Sell'] = get_signal(new_df, 80, 20)[1]
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

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

