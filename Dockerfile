FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY config.py.example /app/config/config.py.example
COPY handlers /app/handlers
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt
COPY *.py /app/
CMD ["python", "bot.py"]
