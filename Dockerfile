# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# アプリケーションのソースコードをコンテナにコピー
COPY app/ /app/

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションを実行
CMD ["python", "main.py"]
