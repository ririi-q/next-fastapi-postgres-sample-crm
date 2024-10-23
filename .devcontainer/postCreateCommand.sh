#!/bin/bash

echo "postCreateCommand.sh start"

cd backend

# Poetryの設定
poetry config virtualenvs.in-project true
if [ -f "pyproject.toml" ]; then
    echo "Pythonの依存関係をインストール中..."
    poetry install --no-root
fi

cd ..


cd frontend

if [ -f "package.json" ]; then
    echo "node_modulesをインストール中..."
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



echo "postCreateCommand.sh end"
