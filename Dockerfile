FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY handlers /app/handlers/
COPY *.py /app/
CMD ["python", "bot.py"]
