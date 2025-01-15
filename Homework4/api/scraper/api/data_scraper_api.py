from flask import jsonify
from Homework4.api.scraper import data_bp
from Homework4.api.scraper.model import data_scraper


@data_bp.route('/tickers/scraper/<string:ticker>', methods=['GET'])
def get_scraper_ticker_data(ticker):
    return jsonify(data_scraper.get_ticker_data(ticker)), 200

@data_bp.route('/tickers/scraper/<string:ticker> <string:from_date> <string:to_date>', methods=['GET']) # date format YYYY-MM-DD
def get_scraper_ticker_data_dates(ticker, from_date, to_date):
    return jsonify(data_scraper.get_ticker_data(ticker, from_date, to_date)), 200

