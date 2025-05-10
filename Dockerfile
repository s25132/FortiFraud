FROM python:3.12-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgomp1 \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app/ ./app/

# Set env and run
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]