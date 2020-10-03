FROM python:3.8-buster

ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev && rm -rf /var/lib/apt/lists/*
COPY ./ /root/

RUN pip install --upgrade pip
RUN easy_install distribute
RUN pip install --upgrade distribute
RUN pip install --no-cache-dir -r /root/requirements.txt
RUN chmod +x /root/bot.py

CMD ["/root/bot.py"]
