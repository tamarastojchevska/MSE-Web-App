from flask import jsonify
from Homework4.api.analysis import plot_bp
from Homework4.api.analysis.model.calculations import Calculations
from Homework4.api.analysis.model.plots import Plots


@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/simple')
def simple_moving_average_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    sma_short = Calculations.simple_moving_average(data['Price'], 1)
    sma_medium = Calculations.simple_moving_average(data['Price'], 7)
    sma_long = Calculations.simple_moving_average(data['Price'], 30)
    signals = Calculations.trading_signals_moving_average(sma_short, sma_long)
    return jsonify(Plots.simple_moving_average(data, sma_short, sma_medium, sma_long, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/exponential')
def exponential_moving_average_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    ema_short = Calculations.simple_moving_average(data['Price'], 1)
    ema_medium = Calculations.simple_moving_average(data['Price'], 7)
    ema_long = Calculations.simple_moving_average(data['Price'], 30)
    signals = Calculations.trading_signals_moving_average(ema_short, ema_long)
    return jsonify(Plots.exponential_moving_average(data, ema_short, ema_medium, ema_long, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/cumulative')
def cumulative_moving_average_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    cma = Calculations.cumulative_moving_average(data['Price'])
    return jsonify(Plots.cumulative_moving_average(data, cma))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/weighted')
def weighted_moving_average_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    signals = Calculations.weighted_moving_average_trading_signals(data['Price'])
    return jsonify(Plots.weighted_moving_average(data['Price'], signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/convergence-divergence')
def moving_average_convergence_divergence_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    macd = Calculations.moving_average_convergence_divergence(data['Price'])
    ema_medium = Calculations.simple_moving_average(data['Price'], 7)
    return jsonify(Plots.moving_average_convergence_divergence(data, macd, ema_medium))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/moving-average/ribbon')
def ribbon_moving_average_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    sma_medium = Calculations.simple_moving_average(data['Price'], 7)
    ema_medium = Calculations.simple_moving_average(data['Price'], 7)
    cma = Calculations.cumulative_moving_average(data['Price'])
    macd = Calculations.moving_average_convergence_divergence(data['Price'])
    return jsonify(Plots.ribbon_moving_averages(data['Price'], sma_medium, ema_medium, cma, macd))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/relative-strength-index')
def relative_strength_index_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    rsi = Calculations.relative_strength_index(data['Price'])
    return jsonify(Plots.relative_strength_index(data['Price'], rsi))


@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/average-directional-index')
def average_directional_index_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    adx = Calculations.average_directional_index(data['Max'], data['Min'], data['Price'])
    return Plots.average_directional_index(data['Price'], adx)


@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/commodity-channel-index')
def commodity_channel_index_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    cci = Calculations.commodity_channel_index(data['Max'], data['Min'], data['Price'])
    return jsonify(Plots.commodity_channel_index(data['Price'], cci))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/index/money-flow-index')
def money_flow_index_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    mfi = Calculations.money_flow_index(data['Max'], data['Min'], data['Price'], data['Volume'])
    signals = Calculations.trading_signals_money_flow_index(data['Max'], data['Min'], data['Price'], mfi)
    return jsonify(Plots.money_flow_index(data, mfi, signals))

@plot_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
               '/plot/oscillator/stochastic')
def stochastic_oscillator_plot(ticker, from_date, to_date):
    data = Plots.get_data(ticker, from_date, to_date)
    stochastic = Calculations.stochastic_oscillator(data['Max'], data['Min'], data['Price'])
    sma_50 = Calculations.simple_moving_average(data['Price'], 50)
    sma_200 = Calculations.simple_moving_average(data['Price'], 200)
    return jsonify(Plots.stochastic_oscillator(data, stochastic, sma_50, sma_200))

