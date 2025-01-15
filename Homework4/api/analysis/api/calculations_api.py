from flask import jsonify
from Homework4.api.analysis import calculations_bp
from Homework4.api.analysis.model import data_preparation, calculations


@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/simple/<string:days>')
def simple_moving_average(ticker, from_date, to_date, days):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.simple_moving_average(data['Price'], int(days)).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/exponential/<string:days>')
def exponential_moving_average(ticker, from_date, to_date, days):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.exponential_moving_average(data['Price'], int(days)).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/cumulative')
def cumulative_moving_average(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.cumulative_moving_average(data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/weighted/signals')
def weighted_moving_average_signals(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.weighted_moving_average_trading_signals(data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/convergence-divergence')
def moving_average_convergence_divergence(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.moving_average_convergence_divergence(data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/relative-strength-index')
def relative_strength_index(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.relative_strength_index(data['Price']))

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/average_directional_index')
def average_directional_index(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.average_directional_index(data['Max'], data['Min'], data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/commodity-channel-index')
def commodity_channel_index(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.commodity_channel_index(data['Max'], data['Min'], data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/money-flow-index')
def money_flow_index(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.money_flow_index(data).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/oscillator/stochastic-oscillator')
def stochastic_oscillator(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    return jsonify(calculations.stochastic_oscillator(data['Max'], data['Min'], data['Price']).to_json())

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/index/money-flow-index/signals')
def trading_signals_money_flow_index(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    mfi = calculations.money_flow_index(data)
    return jsonify(calculations.trading_signals_money_flow_index(data, mfi, 80, 20))

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/simple/signals')
def trading_signals_moving_average_simple(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    sma_short = calculations.simple_moving_average(data['Price'], 1)
    sma_long = calculations.simple_moving_average(data['Price'], 30)
    return jsonify(calculations.trading_signals_moving_average(sma_short, sma_long))

@calculations_bp.route('/tickers/<string:ticker> <string:from_date> <string:to_date>'
                   '/technical-analysis/moving-average/exponential/signals')
def trading_signals_moving_average_exponential(ticker, from_date, to_date):
    data = data_preparation.get_data(ticker, from_date, to_date)
    ema_short = calculations.exponential_moving_average(data['Price'], 1)
    ema_long = calculations.exponential_moving_average(data['Price'], 30)
    return jsonify(calculations.trading_signals_moving_average(ema_short, ema_long))

