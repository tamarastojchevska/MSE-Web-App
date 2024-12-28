from flask import Flask, render_template, request
from flask import send_from_directory
from Homework1.scraper import get_codes
from Homework3.chart_indicators import *

TODAY = date.strftime(date.today(), '%Y-%m-%d')
UPLOAD_FOLDER = '../../Homework1/database/'
app = Flask(__name__, static_folder='./Homework1/database/')

@app.route("/download<path:filename>", methods=["GET"])
def download(filename):
    directory = '../Homework1/database/'

    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/', methods=['GET'])
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
    return render_template('test.html', codes=codes, table=table, filename=filename)

@app.route('/chart', methods=['GET'])
def get_chart():
    codes = get_codes()
    table_name = request.args.get('codes')
    if table_name is None:
        table_name = 'ADIN'

    fromdate = request.args.get("fromdate")
    todate = request.args.get("todate")

    option = request.args.get('chart_option')

    plot = None

    match option:
        case 'SMA':
            plot = simple_moving_average(fromdate, todate, table_name)
        case 'EMA':
            plot = exponential_moving_average(fromdate, todate, table_name)
        case 'WMA':
            plot = weighted_moving_average(fromdate, todate, table_name)
        case 'MACD':
            plot = macd(fromdate, todate, table_name)
        case 'CMA':
            plot = cumulative_moving_average(fromdate, todate, table_name)
        case 'ADX':
            plot = adx_indicator(fromdate, todate, table_name)
        case 'RSI':
            plot = rsi(fromdate, todate, table_name)
        case 'CCI':
            plot = chart_cci(fromdate, todate, table_name)
        case 'MFI':
            plot = money_fow_index(fromdate, todate, table_name)
        case 'RIBBON MA':
            plot = ribbon_moving_averages(fromdate, todate, table_name)
        case 'STOCHASTIC':
            plot = stochastic_oscillator(fromdate, todate, table_name)


    return render_template('test.html', codes=codes, graphJSON=plot)

if __name__ == '__main__':
    app.run(debug=True)