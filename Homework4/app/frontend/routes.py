import json
from datetime import date, timedelta
import requests
from Homework4.app.service import api_urls
from Homework4.app.frontend import templates_bp
from flask import render_template, request, session

TODAY = date.today()


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

@templates_bp.route('/historical-values', methods=['GET'])
def historical_values():
    translations = get_translations()

    tickers = requests.get(api_urls.tickers_url).json()
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
        table = requests.get(api_urls.sqlite_data_url + ticker + ' ' + from_date + ' ' + to_date).json()

    return render_template('historical_values.html',
                           tickers=tickers,
                           table=table,
                           from_date=from_date,
                           to_date=to_date,
                           translations=translations)

@templates_bp.route('/technical-analysis', methods=['GET'])
def technical_analysis():
    message = ''
    plot, req = None, None

    translations = get_translations()

    tickers = requests.get(api_urls.tickers_url).json()
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
            ticker_plot_url = ('http://127.0.0.1:5000/tickers/'
                               + ticker + ' '
                               + from_date + ' '
                               + to_date
                               + '/plot')

            match option:
                case 'SMA':
                    req = requests.get(ticker_plot_url + '/moving-average/simple')
                case 'EMA':
                    req = requests.get(ticker_plot_url + '/moving-average/exponential')
                case 'WMA':
                    req = requests.get(ticker_plot_url + '/moving-average/weighted')
                case 'MACD':
                    req = requests.get(ticker_plot_url + '/moving-average/convergence-divergence')
                case 'CMA':
                    req = requests.get(ticker_plot_url + '/moving-average/cumulative')
                case 'ADX':
                    req = requests.get(ticker_plot_url + '/index/average-directional-index')
                case 'RSI':
                    req = requests.get(ticker_plot_url + '/index/relative-strength-index')
                case 'CCI':
                    req = requests.get(ticker_plot_url + '/index/commodity-channel-index')
                case 'MFI':
                    req = requests.get(ticker_plot_url + '/index/money-flow-index')
                case 'RIBBON MA':
                    req = requests.get(ticker_plot_url + '/moving-average/ribbon')
                case 'STOCHASTIC':
                    req = requests.get(ticker_plot_url + '/oscillator/stochastic')

    if  req is not None:
        if req.status_code == 200:
            plot = req.json()
        elif req.status_code == 204:
            message = f'No data found for {from_date} and {to_date}'

    return render_template('technical_analysis.html',
                           tickers=tickers,
                           graphJSON=plot,
                           from_date=from_date,
                           to_date=to_date,
                           message=message,
                           translations=translations)

