FROM python:3.8-buster

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev && rm -rf /var/lib/apt/lists/*
COPY ./ /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN chmod +x /app/bot.py

CMD ["/app/bot.py"]
