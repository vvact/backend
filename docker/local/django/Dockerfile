FROM python:3.10-slim-buster

# Define environment variables
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Create directories
RUN mkdir -p $APP_HOME/staticfiles

# Metadata
LABEL maintainer="vbm7752@.com"
LABEL description="Development image for Ecomerec E-commerce Project"

# Python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     libpq-dev \
     netcat \
     gettext \
     gcc \
     postgresql \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy entrypoints and make them executable
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker && chmod +x /start-celeryworker

COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower && chmod +x /start-flower

# Copy app source code
COPY . .

# Entrypoint
ENTRYPOINT ["/entrypoint"]
