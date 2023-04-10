FROM python:3.10-alpine

COPY . /influxdb_service

WORKDIR /influxdb_service

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
