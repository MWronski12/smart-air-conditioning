FROM python:3.10-alpine

COPY . /user_api

WORKDIR /user_api

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
