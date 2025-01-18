FROM python:3.10.11-alpine3.17

WORKDIR /update
COPY . /update

RUN pip install -r requirements.txt

CMD ["python", "update_database.py"]