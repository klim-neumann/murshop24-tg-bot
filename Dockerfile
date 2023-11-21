FROM python:3.11

WORKDIR /usr/src/murshop24-tg-bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY murshop24_tg_bot murshop24_tg_bot

EXPOSE 8080

CMD [ "python", "murshop24_tg_bot" ]
