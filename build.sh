#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# ↓ テストデータ作成（1回実行したら必ず削除する）
python manage.py create_testdata ayumikatada@gmail.com