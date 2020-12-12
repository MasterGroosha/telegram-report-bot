# Using separate image as to reduce final image size
FROM python:3.8-slim-buster as compile-image
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# "production" image
FROM python:3.8-slim-buster
COPY --from=compile-image /opt/venv /opt/venv
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"
COPY handlers /app/handlers
COPY *.py /app/
CMD ["python", "bot.py"]