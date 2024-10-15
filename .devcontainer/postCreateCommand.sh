#!/bin/bash

echo "postCreateCommand.sh start"

# install poetry
curl -sSL https://install.python-poetry.org | python3 -

cd backend

# Poetryの設定
poetry config virtualenvs.in-project true
if [ -f "pyproject.toml" ]; then
    poetry install
fi

cd ..


cd frontend

if [ -f "package.json" ]; then
    npm install
fi

cd ..

python3 --version
node --version
npm --version
poetry --version
terraform --version
aws --version

echo "postCreateCommand.sh end"
