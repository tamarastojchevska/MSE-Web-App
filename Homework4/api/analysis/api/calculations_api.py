from flask import jsonify
from Homework4.api.analysis import calculations_bp
from Homework4.api.analysis.model.calculations import Calculations


@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/simple/<string:days>')
def simple_moving_average(ticker, from_date, to_date, days):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.simple_moving_average(data['Price'], int(days)).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/exponential/<string:days>')
def exponential_moving_average(ticker, from_date, to_date, days):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.exponential_moving_average(data['Price'], int(days)).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/cumulative')
def cumulative_moving_average(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.cumulative_moving_average(data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/weighted/signals')
def weighted_moving_average_signals(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.weighted_moving_average_trading_signals(data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/convergence-divergence')
def moving_average_convergence_divergence(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.moving_average_convergence_divergence(data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/relative-strength-index')
def relative_strength_index(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.relative_strength_index(data['Price']))

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/average_directional_index')
def average_directional_index(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.average_directional_index(data['Max'], data['Min'], data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/commodity-channel-index')
def commodity_channel_index(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.commodity_channel_index(data['Max'], data['Min'], data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/money-flow-index')
def money_flow_index(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.money_flow_index(data['Max'], data['Min'], data['Price'], data['Volume']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/oscillator/stochastic-oscillator')
def stochastic_oscillator(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    return jsonify(Calculations.stochastic_oscillator(data['Max'], data['Min'], data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/money-flow-index/signals')
def trading_signals_money_flow_index(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    mfi = Calculations.money_flow_index(data['Max'], data['Min'], data['Price'], data['Volume'])
    return jsonify(Calculations.trading_signals_money_flow_index(mfi, data['Price'], 80, 20))

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/simple/signals')
def trading_signals_moving_average_simple(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    sma_short = Calculations.simple_moving_average(data['Price'], 1)
    sma_long = Calculations.simple_moving_average(data['Price'], 30)
    return jsonify(Calculations.trading_signals_moving_average(sma_short, sma_long))

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/exponential/signals')
def trading_signals_moving_average_exponential(ticker, from_date, to_date):
    data = Calculations.get_data(ticker, from_date, to_date)
    ema_short = Calculations.exponential_moving_average(data['Price'], 1)
    ema_long = Calculations.exponential_moving_average(data['Price'], 30)
    return jsonify(Calculations.trading_signals_moving_average(ema_short, ema_long))

