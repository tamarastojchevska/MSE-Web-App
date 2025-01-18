import json
from datetime import date, timedelta
import requests
from flask import render_template, request, session, send_from_directory
from . import templates_bp
from models.analysis.model.data_preparation import get_data
from models.sqlite.sqlite_database import get_sqlite_ticker_data
from models.analysis.chart_plots import *


TODAY = date.today()
DOWNLOAD_FOLDER = './csv_database'
db_path = 'database.db'
TICKER_URL = 'http://scraper:5001/scraper/tickers'

def load_translations_file(lang):
    path = './templates/translations/'+lang+'.json'
    with open(path, encoding="utf8") as f:
        return json.load(f)

def set_lang_session():
    session.permanent = False
    lang = request.args.get('lang')

    if session.get('lang') is None:
        session['lang'] = 'en'

    if lang is None:
        lang = session.get('lang')

    session['lang'] = lang
    return lang

def get_translations():
    return load_translations_file(set_lang_session())


@templates_bp.route('/', methods=['GET'])
def index():
    translations = get_translations()
    return render_template('index.html',
                           translations=translations)

@templates_bp.route('/about-us', methods=['GET'])
def about_us():
    translations = get_translations()
    return render_template('about_us.html',
                           translations=translations)

@templates_bp.route('/csv/download/<path:filename>', methods = ['GET'])
def csv_data_download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@templates_bp.route('/historical-values', methods=['GET'])
def historical_values():
    translations = get_translations()

    tickers = requests.get(TICKER_URL).json()
    ticker = request.args.get('tickers')
    if ticker is None:
        ticker = tickers[0]

    table = []

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    if from_date is None and to_date is None:
        from_date = (TODAY - timedelta(days=30)).strftime("%Y-%m-%d")
        to_date = TODAY.strftime("%Y-%m-%d")

    if from_date is not None and to_date is not None and from_date < to_date:
        table = get_sqlite_ticker_data(db_path, ticker, from_date, to_date)

    filename = ticker + '.csv_data'

    return render_template('historical_values.html',
                           tickers=tickers,
                           table=table,
                           from_date=from_date,
                           to_date=to_date,
                           filename=filename,
                           translations=translations)

@templates_bp.route('/technical-analysis', methods=['GET'])
def technical_analysis():
    message = ''
    plot, req = None, None

    translations = get_translations()

    tickers = requests.get(TICKER_URL).json()
    ticker = request.args.get('tickers')
    if ticker is None:
        ticker = tickers[0]

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    option = request.args.get('plot_option')

    if from_date is not None and to_date is not None:
        if from_date > to_date or from_date == "" and to_date == "":
            message = "Please enter valid dates."
        else:
            data = get_data(db_path, ticker, from_date, to_date)
            if data.empty:
                message = f'No data available for dates between {from_date} and {to_date}'
            else:
                match option:
                    case 'SMA':
                        plot = simple_moving_average_plot(data)
                    case 'EMA':
                        plot = exponential_moving_average_plot(data)
                    case 'WMA':
                        plot = weighted_moving_average_plot(data)
                    case 'MACD':
                        plot = moving_average_convergence_divergence_plot(data)
                    case 'CMA':
                        plot = cumulative_moving_average_plot(data)
                    case 'ADX':
                        plot = average_directional_index_plot(data)
                    case 'RSI':
                        plot = relative_strength_index_plot(data)
                    case 'CCI':
                        plot = commodity_channel_index_plot(data)
                    case 'MFI':
                        plot = money_flow_index_plot(data)
                    case 'RIBBON MA':
                        plot = ribbon_moving_average_plot(data)
                    case 'STOCHASTIC':
                        plot = stochastic_oscillator_plot(data)


    return render_template('technical_analysis.html',
                           tickers=tickers,
                           graphJSON=plot,
                           from_date=from_date,
                           to_date=to_date,
                           message=message,
                           translations=translations)

