FROM python:3.10-alpine

COPY influxdb/ /app/influxdb/
COPY protos/ /app/protos/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/influxdb

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/*.proto

CMD [ "python", "./main.py" ]
