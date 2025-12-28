FROM python:3.11-slim

# Set up working dir
WORKDIR /app

# Install build deps and system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# Create a non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_conf.py", "app:app"]
