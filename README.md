# acm

# Usage
## Dockerをインストール
### Dockerの公式サイトからDocker Desktopをダウンロードします。
- Docker Desktop for Windows
### インストールパッケージを開いて指示に従ってインストール
### インストール完了後、Docker Desktopを起動
### インストール確認
### WindowsのコマンドプロンプトまたはPowerShellを開いて以下を実行します：
- sh
- docker --version
## コンテナをビルドして走らせる
- docker run hello-world
- docker build -t chatbot .
- docker run -it --rm -v "$(pwd):/" -e OPENAI_API_KEY=<ここはAPIキーを入力してください> chatbot