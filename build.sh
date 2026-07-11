#!/usr/bin/env bash
# Exit on error
set -o errexit

# パッケージをインストール
pip install -r requirements.txt

# Node.jsとnpmがインストールされている前提
(cd theme/static_src && npm install)
python manage.py tailwind build

# 静的ファイルを収集
python manage.py collectstatic --no-input

# データベースマイグレーションを実行
python manage.py migrate