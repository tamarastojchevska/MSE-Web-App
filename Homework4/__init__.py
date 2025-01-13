from flask import Flask

from Homework4.api.scraper.api import data_scraper_api
from Homework4.frontend import routes as templates_api
from Homework4.api.sqlite.api import sqlite_api
from Homework4.api.analysis.api import calculations_api, plots_api
from Homework4.api.tickers.api import tickers_api
from Homework4.api.csv.api import csv_data_api

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

app.register_blueprint(data_scraper_api.data_bp)
app.register_blueprint(templates_api.templates_bp)
app.register_blueprint(sqlite_api.sqlite_bp)
app.register_blueprint(plots_api.plot_bp)
app.register_blueprint(calculations_api.calculations_bp)
app.register_blueprint(tickers_api.tickers_bp)
app.register_blueprint(csv_data_api.csv_data_bp)
