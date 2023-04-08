FROM python:3.10-alpine

COPY app_service/ /app/app_service/
COPY protos/ /app/protos/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/app_service

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc -I../protos --python_out=./app --grpc_python_out=./app ../protos/*.proto

CMD [ "python", "./main.py" ]
