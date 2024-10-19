# /workspaceで実行

## コンテナを再ビルドしてバックエンドで 起動
docker-compose -f docker/dev/compose.yml down --rmi all
docker-compose -f docker/dev/compose.yml build --no-cache
docker-compose -f docker/dev/compose.yml up -d

## コンテナの状態を確認
docker-compose -f docker/dev/compose.yml ps

## バックエンドのコンテナを再起動
docker-compose -f docker/dev/compose.yml restart backend

## バックエンドのコンテナを停止
docker-compose -f docker/dev/compose.yml stop backend

## バックエンドのコンテナに入る
docker-compose -f docker/dev/compose.yml exec backend /bin/bash

## フロントエンドのコンテナに入る
docker-compose -f docker/dev/compose.yml exec frontend /bin/bash

## データベースのコンテナに入る
docker-compose -f docker/dev/compose.yml exec db /bin/bash

## データベースに入る
docker-compose -f docker/dev/compose.yml exec db psql -U postgres -d postgres

## 一通りのデータベースの操作コマンド
\d # テーブル一覧
\l # データベース一覧
\c app # データベースに接続
\dt # テーブル一覧
\q # データベースから出る

## 一通りのSQL操作コマンド
SELECT * FROM users;
INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com');
UPDATE users SET email = 'john.doe@example.com' WHERE name = 'John Doe';
DELETE FROM users WHERE name = 'John Doe';


## Dev環境でのマイグレーション
docker-compose -f docker/dev/compose.yml exec backend /bin/bash
poetry run alembic init alembic #マイグレーションファイルを作成
poetry run alembic revision --autogenerate -m "描画的なマイグレーション名" #マイグレーションファイルを作成
poetry run alembic upgrade head #マイグレーションを適用
poetry run alembic downgrade -1 #前のマイグレーションにダウングレード
poetry run alembic downgrade <revision> #指定したマイグレーション番号にダウングレード
poetry run alembic current #現在のマイグレーション番号
poetry run alembic history #マイグレーションの履歴
poetry run alembic heads #次のマイグレーション番号
poetry run alembic upgrade head --sql > migration.sql


## FastApi Docs
http://localhost:5000/docs

## Frontend
http://localhost:3000/