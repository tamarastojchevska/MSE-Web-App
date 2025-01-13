import os

from flask import send_from_directory, request, jsonify
from Homework4.CSVdataService import csv_data_bp

DOWNLOAD_FOLDER = './csv_database'


@csv_data_bp.route('/csv/download', methods = ['GET'])
def csv_data_download():
    filename = request.args.get('filename')
    if filename == "":
       filename = os.listdir(DOWNLOAD_FOLDER)[0]
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
