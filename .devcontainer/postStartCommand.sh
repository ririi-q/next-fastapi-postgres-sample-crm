#!/bin/bash

echo "postStartCommand.sh start"

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

echo "postStartCommand.sh end"