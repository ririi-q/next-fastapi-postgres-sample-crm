# db/Dockerfile
FROM postgres:17
ENV POSTGRES_DB=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# 初期化スクリプトをコンテナにコピー
COPY init.sql /docker-entrypoint-initdb.d/