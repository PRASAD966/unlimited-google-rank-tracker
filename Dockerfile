# Use official Playwright image (matches installed version 1.57.0)
FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

# Set working directory
WORKDIR /app

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    default-libmysqlclient-dev \
    build-essential \
    dbus \
    dbus-x11 \
    curl \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Brave Browser
RUN curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main"|tee /etc/apt/sources.list.d/brave-browser-release.list && \
    apt-get update && \
    apt-get install -y brave-browser x11vnc fluxbox

# Fix for DBus errors in Playwright
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment Configuration for Linux
ENV BRAVE_PATH=/usr/bin/brave-browser
ENV EXTENSION_PATH=/app/extensions/raptor_unpacked
ENV DISPLAY=:99
ENV MAX_CONCURRENT_TASKS=40
ENV DB_HOST=db
ENV DB_USER=user
ENV DB_PASS=password
ENV DB_NAME=rankplex_db

# Start command
CMD xvfb-run --auto-servernum --server-args="-screen 0 1280x1024x24" python server.py
