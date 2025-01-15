from flask import Flask
from Homework4.app.service.tickers.api.tickers_api import tickers_bp

app = Flask(__name__)
app.register_blueprint(tickers_bp)

app.run(debug=True, port=5001)