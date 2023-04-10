FROM python:3.10-alpine

COPY . /mqtt_service

WORKDIR /mqtt_service

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
