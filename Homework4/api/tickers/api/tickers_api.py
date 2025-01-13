from Homework4.api.tickers import tickers_bp
from Homework4.api.tickers.model.tickers import TickerScraper

@tickers_bp.route('/tickers', methods=['GET'])
def get_tickers():
    return TickerScraper.scrape_tickers()

