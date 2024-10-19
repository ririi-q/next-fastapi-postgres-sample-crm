#!/bin/bash

set -e

# データベースの準備ができるまで待機
echo "データベースの準備を待っています..."
until poetry run python -c "import psycopg2; psycopg2.connect(host='db', dbname='postgres', user='postgres', password='postgres')" 2>/dev/null
do
  echo "データベースに接続できません。再試行します..."
  sleep 1
done

echo "データベースの準備が完了しました！"

# マイグレーションの初期化（必要な場合）
if [ ! -d "alembic" ]; then
  echo "マイグレーションを初期化しています..."
  poetry run alembic init alembic
fi

# マイグレーションの生成（必要な場合）
if [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
  echo "初期マイグレーションを生成しています..."
  poetry run alembic revision --autogenerate -m "Initial migration"
fi

# マイグレーションの適用
echo "マイグレーションを適用しています..."
poetry run alembic upgrade head

echo "マイグレーションが完了しました！"
