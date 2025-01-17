from Homework4.app.models.analysis.model import plots, calculations


def simple_moving_average_plot(data):
    sma_short = calculations.simple_moving_average(data['Price'], 1)
    sma_medium = calculations.simple_moving_average(data['Price'], 7)
    sma_long = calculations.simple_moving_average(data['Price'], 30)
    signals = calculations.trading_signals_moving_average(sma_short, sma_long)
    return plots.simple_moving_average(data, sma_short, sma_medium, sma_long, signals)


def exponential_moving_average_plot(data):
    ema_short = calculations.simple_moving_average(data['Price'], 1)
    ema_medium = calculations.simple_moving_average(data['Price'], 7)
    ema_long = calculations.simple_moving_average(data['Price'], 30)
    signals = calculations.trading_signals_moving_average(ema_short, ema_long)
    return plots.exponential_moving_average(data, ema_short, ema_medium, ema_long, signals)


def cumulative_moving_average_plot(data):
    cma = calculations.cumulative_moving_average(data['Price'])
    return plots.cumulative_moving_average(data, cma)


def weighted_moving_average_plot(data):
    signals = calculations.weighted_moving_average_trading_signals(data['Price'])
    return plots.weighted_moving_average(data, signals)


def moving_average_convergence_divergence_plot(data):
    macd = calculations.moving_average_convergence_divergence(data['Price'])
    ema_medium = calculations.simple_moving_average(data['Price'], 7)
    return plots.moving_average_convergence_divergence(data, macd, ema_medium)


def ribbon_moving_average_plot(data):
    sma_medium = calculations.simple_moving_average(data['Price'], 7)
    ema_medium = calculations.simple_moving_average(data['Price'], 7)
    cma = calculations.cumulative_moving_average(data['Price'])
    macd = calculations.moving_average_convergence_divergence(data['Price'])
    return plots.ribbon_moving_averages(data, sma_medium, ema_medium, cma, macd)


def relative_strength_index_plot(data):
    rsi = calculations.relative_strength_index(data['Price'])
    return plots.relative_strength_index(data, rsi)


def average_directional_index_plot(data):
    adx = calculations.average_directional_index(data['Max'], data['Min'], data['Price'])
    return plots.average_directional_index(data, adx)


def commodity_channel_index_plot(data):
    cci = calculations.commodity_channel_index(data['Max'], data['Min'], data['Price'])
    return plots.commodity_channel_index(data, cci)


def money_flow_index_plot(data):
    mfi = calculations.money_flow_index(data)
    signals = calculations.trading_signals_money_flow_index(data, mfi, )
    return plots.money_flow_index(data, mfi, signals)


def stochastic_oscillator_plot(data):
    stochastic = calculations.stochastic_oscillator(data['Max'], data['Min'], data['Price'])
    sma_50 = calculations.simple_moving_average(data['Price'], 50)
    sma_200 = calculations.simple_moving_average(data['Price'], 200)
    return plots.stochastic_oscillator(data, stochastic, sma_50, sma_200)
