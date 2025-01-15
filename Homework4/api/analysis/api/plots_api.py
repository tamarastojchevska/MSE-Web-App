from flask import jsonify
from Homework4.api.analysis import plot_bp
from Homework4.api.analysis.model import data_preparation, calculations, plots


@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/simple')
def simple_moving_average_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    sma_short = calculations.simple_moving_average(data['Price'], 1)
    sma_medium = calculations.simple_moving_average(data['Price'], 7)
    sma_long = calculations.simple_moving_average(data['Price'], 30)
    signals = calculations.trading_signals_moving_average(sma_short, sma_long)
    return jsonify(plots.simple_moving_average(data, sma_short, sma_medium, sma_long, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/exponential')
def exponential_moving_average_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    ema_short = calculations.simple_moving_average(data['Price'], 1)
    ema_medium = calculations.simple_moving_average(data['Price'], 7)
    ema_long = calculations.simple_moving_average(data['Price'], 30)
    signals = calculations.trading_signals_moving_average(ema_short, ema_long)
    return jsonify(plots.exponential_moving_average(data, ema_short, ema_medium, ema_long, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/cumulative')
def cumulative_moving_average_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    cma = calculations.cumulative_moving_average(data['Price'])
    return jsonify(plots.cumulative_moving_average(data, cma))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/weighted')
def weighted_moving_average_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    signals = calculations.weighted_moving_average_trading_signals(data['Price'])
    return jsonify(plots.weighted_moving_average(data, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/convergence-divergence')
def moving_average_convergence_divergence_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    macd = calculations.moving_average_convergence_divergence(data['Price'])
    ema_medium = calculations.simple_moving_average(data['Price'], 7)
    return jsonify(plots.moving_average_convergence_divergence(data, macd, ema_medium))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/ribbon')
def ribbon_moving_average_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    sma_medium = calculations.simple_moving_average(data['Price'], 7)
    ema_medium = calculations.simple_moving_average(data['Price'], 7)
    cma = calculations.cumulative_moving_average(data['Price'])
    macd = calculations.moving_average_convergence_divergence(data['Price'])
    return jsonify(plots.ribbon_moving_averages(data, sma_medium, ema_medium, cma, macd))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/relative-strength-index')
def relative_strength_index_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    rsi = calculations.relative_strength_index(data['Price'])
    return jsonify(plots.relative_strength_index(data, rsi))


@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/average-directional-index')
def average_directional_index_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    adx = calculations.average_directional_index(data['Max'], data['Min'], data['Price'])
    return jsonify(plots.average_directional_index(data, adx))


@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/commodity-channel-index')
def commodity_channel_index_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    cci = calculations.commodity_channel_index(data['Max'], data['Min'], data['Price'])
    return jsonify(plots.commodity_channel_index(data, cci))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/money-flow-index')
def money_flow_index_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    mfi = calculations.money_flow_index(data)
    signals = calculations.trading_signals_money_flow_index(data, mfi, )
    return jsonify(plots.money_flow_index(data, mfi, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/oscillator/stochastic')
def stochastic_oscillator_plot(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    stochastic = calculations.stochastic_oscillator(data['Max'], data['Min'], data['Price'])
    sma_50 = calculations.simple_moving_average(data['Price'], 50)
    sma_200 = calculations.simple_moving_average(data['Price'], 200)
    return jsonify(plots.stochastic_oscillator(data, stochastic, sma_50, sma_200))

