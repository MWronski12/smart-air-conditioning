FROM python:3.10-alpine

COPY mqtt/ /app/mqtt/
COPY protos/ /app/protos/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/mqtt

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/mqtt.proto

CMD [ "python", "./main.py" ]
