FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY bot.py .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -u 1000 -U botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python", "bot.py"]