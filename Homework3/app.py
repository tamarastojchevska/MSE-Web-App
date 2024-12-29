from flask import Flask, render_template, request, send_from_directory, session
from Homework1.scraper import get_codes
from datetime import date
import sqlite3
from Homework3.chart_indicators import *
from Homework3.scraper import get_issuers
from Homework3.sqlite_database import *


TODAY = date.strftime(date.today(), '%Y-%m-%d')
UPLOAD_FOLDER = '../../Homework1/database/'

def load_translations(lang):
    path = './templates/'+lang+'.json'
    with open(path, encoding="utf8") as f:
        return json.load(f)

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

@app.route('/')
def index():
    session.permanent = False
    lang = request.args.get('lang')
    if session.get('lang') is None:
        session['lang'] = 'en'
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    return render_template('index.html', translations=translations)

@app.route('/aboutus')
def aboutus():
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    return render_template('aboutus.html', translations=translations)

@app.route("/download <path:filename>", methods=["GET"])
def download(filename):
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    return send_from_directory(UPLOAD_FOLDER, filename, translations=translations)

@app.route('/hystoricalValues', methods=['GET'])
def get_table():
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    codes = get_issuers()
    table_name = request.args.get('codes')
    if table_name is None:
        table_name = codes[0]

    file = 'database.db'
    connection = sqlite3.connect(file)
    cursor = connection.cursor()

    fromdate = request.args.get("fromdate")
    todate = request.args.get("todate")

    if fromdate is None:
        fromdate = TODAY
    if todate is None:
        todate = TODAY

    cursor.execute("SELECT * from %s WHERE DateFormated > ? AND DateFormated < ?" % table_name, [fromdate, todate])
    table = cursor.fetchall()
    filename = table_name+'.csv'

    return render_template('historicalValues.html', codes=codes, table=table, filename=filename, translations=translations)

@app.route('/marketInsights', methods=['GET'])
def get_chart():
    session.permanent = False
    lang = request.args.get('lang')
    if lang is None:
        lang = session.get('lang')
    session['lang'] = lang
    translations = load_translations(lang)
    codes = get_issuers()
    table_name = request.args.get('codes')
    if table_name is None:
        table_name = codes[0]

    fromdate = request.args.get("fromdate")
    todate = request.args.get("todate")

    option = request.args.get('chart_option')

    plot = None
    message = ''

    data = get_data(fromdate, todate, table_name)
    if not data.empty:
        match option:
            case 'SMA':
                plot = simple_moving_average(data)
            case 'EMA':
                plot = exponential_moving_average(data)
            case 'WMA':
                plot = weighted_moving_average(data)
            case 'MACD':
                plot = macd(data)
            case 'CMA':
                plot = cumulative_moving_average(data)
            case 'ADX':
                plot = adx_indicator(data)
            case 'RSI':
                plot = rsi(data)
            case 'CCI':
                plot = chart_cci(data)
            case 'MFI':
                plot = money_fow_index(data)
            case 'RIBBON MA':
                plot = ribbon_moving_averages(data)
            case 'STOCHASTIC':
                plot = stochastic_oscillator(data)
    else:
        if fromdate is not None and todate is not None:
            message = f'No data found for date {fromdate} and date {todate} for issuer {table_name}'

    return render_template('technicalAnalysis.html', codes=codes, graphJSON=plot, message=message, translations=translations)

if __name__ == '__main__':
    # main_db('database')
    app.run(debug=True)

