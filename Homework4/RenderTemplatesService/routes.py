import json
from datetime import date, timedelta

import requests
from Homework4.RenderTemplatesService import templates_bp
from flask import render_template, request, session

TODAY = date.today()
tickers_api_url = 'http://127.0.0.1:5000/tickers'
sqlite_ticker_data_url = 'http://127.0.0.1:5000/tickers/sqlite/'

def load_translations(lang):
    path = './RenderTemplatesService/templates/translations/'+lang+'.json'
    with open(path, encoding="utf8") as f:
        return json.load(f)

@templates_bp.route('/', methods=['GET'])
def index():
    session.permanent = False
    lang = request.args.get('lang')
    if session.get('lang') is None:
        session['lang'] = 'en'
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    return render_template('index.html',
                           translations=translations)

@templates_bp.route('/about-us', methods=['GET'])
def about_us():
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    return render_template('about_us.html',
                           translations=translations)

@templates_bp.route('/historical-values', methods=['GET'])
def historical_values():
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)

    tickers = requests.get(tickers_api_url).json()
    ticker = request.args.get('tickers')
    if ticker is None:
        ticker = tickers[0]

    table = []

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    if from_date is None and to_date is None:
        from_date = (TODAY - timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = TODAY.strftime("%Y-%m-%d")

    if from_date is not None and to_date is not None:
        table = requests.get(sqlite_ticker_data_url + ticker + ' ' + from_date + ' ' + to_date).json()

    return render_template('historical_values.html',
                           tickers=tickers,
                           table=table,
                           from_date=from_date,
                           to_date=to_date,
                           translations=translations)

@templates_bp.route('/technical-analysis', methods=['GET'])
def technical_analysis():
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)

    tickers = requests.get(tickers_api_url).json()
    ticker = request.args.get('tickers')
    if ticker is None:
        ticker = tickers[0]

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    option = request.args.get('plot_option')

    message = ''

    plot = None
    if from_date == "" and to_date == "":
        from_date = None
        to_date = None
        message = "Please enter valid dates."


    if from_date is not None and to_date is not None:
        print('in if statement')
        ticker_plot_url = ('http://127.0.0.1:5000/tickers/'
                           + ticker + ' '
                           + from_date + ' '
                           + to_date
                           + '/plot')

        match option:
            case 'SMA':
                plot = requests.get(ticker_plot_url + '/moving-average/simple').json()
            case 'EMA':
                plot = requests.get(ticker_plot_url + '/moving-average/exponential').json()
            case 'WMA':
                plot = requests.get(ticker_plot_url + '/moving-average/weighted').json()
            case 'MACD':
                plot = requests.get(ticker_plot_url + '/moving-average/convergence-divergence').json()
            case 'CMA':
                plot = requests.get(ticker_plot_url + '/moving-average/cumulative').json()
            case 'ADX':
                plot = requests.get(ticker_plot_url + '/index/average-directional-index').json()
            case 'RSI':
                plot = requests.get(ticker_plot_url + '/index/relative-strength-index').json()
            case 'CCI':
                plot = requests.get(ticker_plot_url + '/index/commodity-channel-index').json()
            case 'MFI':
                plot = requests.get(ticker_plot_url + '/index/money-flow-index').json()
            case 'RIBBON MA':
                plot = requests.get(ticker_plot_url + '/moving-average/ribbon').json()
            case 'STOCHASTIC':
                plot = requests.get(ticker_plot_url + '/oscillator/stochastic').json()
    else:
        if from_date is not None and to_date is not None:
            message = f'No data found for date {from_date} and date {to_date} for issuer {ticker}'

    return render_template('technical_analysis.html',
                           tickers=tickers,
                           graphJSON=plot,
                           from_date=from_date,
                           to_date=to_date,
                           message=message,
                           translations=translations)

