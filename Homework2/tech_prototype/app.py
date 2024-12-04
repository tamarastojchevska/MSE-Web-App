from flask import Flask, render_template, request, send_from_directory
from Homework1.scraper import get_codes
from datetime import date
import sqlite3

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


if __name__ == '__main__':
    app.run(debug=True)

