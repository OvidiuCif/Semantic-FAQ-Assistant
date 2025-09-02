FROM python:3.11-slim

WORKDIR /app

# necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# req.txt + install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# api-port
EXPOSE 8000

# start the API service
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]