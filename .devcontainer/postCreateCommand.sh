#!/bin/bash

echo "postCreateCommand.sh start"

# install poetry
curl -sSL https://install.python-poetry.org | python3 -

cd backend

# Poetryの設定
poetry config virtualenvs.in-project true
if [ -f "pyproject.toml" ]; then
    poetry install --no-root
fi

cd ..


cd frontend

if [ -f "package.json" ]; then
    npm install
fi

cd ..

# バージョン情報出力関数
print_version() {
    echo -e "\e[1;34m$1\e[0m version: \e[1;32m$($2)\e[0m"
}

# かっこいいバージョン情報出力
echo -e "\n\e[1;35m"
cat << "EOF"
 _____           _                                  _   
|_   _|__   ___ | |___    __   _____ _ __ ___  ___ | |_ 
  | |/ _ \ / _ \| / __|___\ \ / / _ \ '__/ __|/ _ \| __|
  | | (_) | (_) | \__ \____\ V /  __/ |  \__ \ (_) | |_ 
  |_|\___/ \___/|_|___/     \_/ \___|_|  |___/\___/ \__|
                                                        
EOF
echo -e "\e[0m"

print_version "Python" "python3 --version | cut -d' ' -f2"
print_version "Poetry" "poetry --version | cut -d' ' -f3"

print_version "Node.js" "node --version"
print_version "npm" "npm --version"
print_version "Next.js" "npx next --version"
print_version "React" "npm react --version"

print_version "Terraform" "terraform --version | head -n1 | cut -d'v' -f2"
print_version "AWS CLI" "aws --version | cut -d' ' -f1 | cut -d'/' -f2"

echo "postCreateCommand.sh end"
