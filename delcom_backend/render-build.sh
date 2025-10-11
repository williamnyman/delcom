#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Install Linux dependencies for headless Chromium
apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    libxcb-shm0 \
    libxcb1 \
    libxfixes3 \
    libxrender1 \
    libxi6 \
    libxext6 \
    libx11-6 \
    libxkbcommon0 \
    libxtst6 \
    lsb-release \
    fonts-noto-color-emoji

# Install Chromium for Playwright
python -m playwright install chromium
