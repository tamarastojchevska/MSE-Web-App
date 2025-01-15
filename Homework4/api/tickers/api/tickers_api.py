from Homework4.api.tickers import tickers_bp
from Homework4.api.tickers.model import tickers

@tickers_bp.route('/tickers', methods=['GET'])
def get_tickers():
    return tickers.scrape_tickers()

