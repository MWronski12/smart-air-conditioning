FROM python:3.10-alpine

COPY . /logic_service

WORKDIR /logic_service

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
