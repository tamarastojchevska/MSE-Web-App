import os

from flask import send_from_directory, request
from Homework4.app.service.csv import csv_data_bp

DOWNLOAD_FOLDER = './csv_database'


@csv_data_bp.route('/csv/download/<path:filename>', methods = ['GET'])
def csv_data_download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
