FROM python:3.10-alpine

COPY . /app_service

WORKDIR /app_service

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
