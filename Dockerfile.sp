FROM python:3.12-slim

WORKDIR /app

# Install Ubuntu OS security libraries required for XML crypto
RUN apt-get update && apt-get install -y xmlsec1 libxmlsec1-dev pkg-config gcc && rm -rf /var/lib/apt/lists/*

# Copy configuration and skeleton workspace
COPY pyproject.toml .
COPY src/ src/

# Install the dependencies globally inside the container
RUN pip install --no-cache-dir .




