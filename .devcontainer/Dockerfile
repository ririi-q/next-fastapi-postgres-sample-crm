FROM python:3.12-slim-bullseye

# Update and install necessary dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Create vscode user and group
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m vscode \
    && apt-get update \
    && apt-get install -y sudo \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the default user to vscode
USER vscode