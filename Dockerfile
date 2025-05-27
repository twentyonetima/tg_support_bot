FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY rq.txt .
RUN pip install --no-cache-dir -r rq.txt

COPY . .

CMD ["python", "main.py"]