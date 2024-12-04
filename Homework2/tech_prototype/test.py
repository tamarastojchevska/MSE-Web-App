from flask import Flask, render_template, request, redirect, session
from Homework1.scraper import get_codes
from datetime import date
import sqlite3
TODAY = date.strftime(date.today(), '%Y-%m-%d')

app = Flask(__name__)


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

    return render_template('test.html', codes=codes, table=table)


if __name__ == '__main__':
    app.run(debug=True)