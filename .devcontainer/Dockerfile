FROM mcr.microsoft.com/devcontainers/base:jammy

# システムの更新とツールのインストール
RUN apt-get update && apt-get install -y \
    docker.io \
    docker-compose \
    wget \
    unzip \
    curl \
    software-properties-common

# AWS CLIのインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# Node.jsのインストール
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Pythonのインストール
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.12 python3.12-venv python3-pip \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && update-alternatives --set python3 /usr/bin/python3.12

# Terraformのインストール
RUN wget https://releases.hashicorp.com/terraform/1.9.7/terraform_1.9.7_linux_amd64.zip \
    && unzip terraform_1.9.7_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_1.9.7_linux_amd64.zip

# TFLintのインストール
RUN curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Terragruntのインストール
RUN wget https://github.com/gruntwork-io/terragrunt/releases/download/v0.52.0/terragrunt_linux_amd64 \
    && mv terragrunt_linux_amd64 /usr/local/bin/terragrunt \
    && chmod +x /usr/local/bin/terragrunt

# キャッシュのクリーンアップ
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
