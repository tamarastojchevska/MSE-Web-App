from flask import jsonify
from __init__ import data_scraper_app
from model import data_scraper
from model import tickers

@data_scraper_app.route('/scraper/tickers', methods=['GET'])
def get_tickers():
    return jsonify(tickers.scrape_tickers())

@data_scraper_app.route('/scraper/<string:ticker>', methods=['GET'])
def get_scraper_ticker_data(ticker):
    return jsonify(data_scraper.get_ticker_data(ticker)), 200

@data_scraper_app.route('/scraper/<string:ticker> <string:from_date> <string:to_date>', methods=['GET']) # date format YYYY-MM-DD
def get_scraper_ticker_data_dates(ticker, from_date, to_date):
    return jsonify(data_scraper.get_ticker_data(ticker, from_date, to_date)), 200

