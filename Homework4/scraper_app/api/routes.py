from flask import jsonify
from Homework4.scraper_app import data_scraper_app
from Homework4.scraper_app.model import data_scraper


@data_scraper_app.route('/scraper/<string:ticker>', methods=['GET'])
def get_scraper_ticker_data(ticker):
    return jsonify(data_scraper.get_ticker_data(ticker)), 200

@data_scraper_app.route('/scraper/<string:ticker> <string:from_date> <string:to_date>', methods=['GET']) # date format YYYY-MM-DD
def get_scraper_ticker_data_dates(ticker, from_date, to_date):
    return jsonify(data_scraper.get_ticker_data(ticker, from_date, to_date)), 200

