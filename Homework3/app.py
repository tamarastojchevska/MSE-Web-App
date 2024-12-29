from flask import Flask, render_template, request, send_from_directory
from Homework1.scraper import get_codes
from datetime import date
import sqlite3
from Homework3.chart_indicators import *
from Homework3.sqlite_database import *

TODAY = date.strftime(date.today(), '%Y-%m-%d')
UPLOAD_FOLDER = '../../Homework1/database/'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route("/download <path:filename>", methods=["GET"])
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/hystoricalValues', methods=['GET'])
def get_table():
    codes = get_codes()
    table_name = request.args.get('codes')
    if table_name is None:
        table_name = 'ADIN'

    file = 'database.db'
    connection = sqlite3.connect(file)
    cursor = connection.cursor()

    fromdate = request.args.get("fromdate")
    todate = request.args.get("todate")

    if fromdate is None:
        fromdate = TODAY
    if todate is None:
        todate = TODAY

    cursor.execute("SELECT * from %s WHERE DateFormated > ? AND DATEfORMATED < ?" % table_name, [fromdate, todate])
    table = cursor.fetchall()
    filename = table_name+'.csv'

    return render_template('historicalValues.html', codes=codes, table=table, filename=filename)

@app.route('/marketInsights', methods=['GET'])
def get_chart():
    codes = get_codes()
    table_name = request.args.get('codes')
    if table_name is None:
        table_name = 'ADIN'

    fromdate = request.args.get("fromdate")
    todate = request.args.get("todate")

    option = request.args.get('chart_option')

    plot = None
    message = ''

    data = get_data(fromdate, todate, table_name)
    if not data.empty:
        match option:
            case 'SMA':
                plot = simple_moving_average(fromdate, todate, data)
            case 'EMA':
                plot = exponential_moving_average(fromdate, todate, data)
            case 'WMA':
                plot = weighted_moving_average(fromdate, todate, data)
            case 'MACD':
                plot = macd(fromdate, todate, data)
            case 'CMA':
                plot = cumulative_moving_average(fromdate, todate, data)
            case 'ADX':
                plot = adx_indicator(fromdate, todate, data)
            case 'RSI':
                plot = rsi(fromdate, todate, data)
            case 'CCI':
                plot = chart_cci(fromdate, todate, data)
            case 'MFI':
                plot = money_fow_index(fromdate, todate, data)
            case 'RIBBON MA':
                plot = ribbon_moving_averages(fromdate, todate, data)
            case 'STOCHASTIC':
                plot = stochastic_oscillator(fromdate, todate, data)
    else:
        if fromdate is not None and todate is not None:
            message = f'No data found for date {fromdate} and date {todate} for issuer {table_name}'

    return render_template('technicalAnalysis.html', codes=codes, graphJSON=plot, message=message)

if __name__ == '__main__':
    # main_db('database')
    app.run(debug=True)

