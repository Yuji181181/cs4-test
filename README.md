# Simple Slack Clone with AI Chat

DjangoとDjango Channelsを使用した、リアルタイムチャット機能を持つSlack風Webアプリケーションです。
WebSocketを使用したリアルタイム通信に加え、Groq APIを利用したAIボットとの会話機能も搭載しています。

## 機能概要

*   **リアルタイムチャット**: WebSocket (Django Channels) を使用し、リロードなしでメッセージを送受信できます。
*   **チャンネル機能**: 複数のチャンネル（部屋）を作成・切り替え可能です。
*   **ユーザー認証**: Django標準の認証システムを使用したサインアップ・ログイン機能。
*   **AIチャットボット**: `#ai-talk` チャンネルでは、AI (Llama 3.3 70B via Groq) が自動で返信します。
*   **レスポンシブデザイン**: Tailwind CSSを使用したモダンなUI。

## 技術スタック

*   **Backend**: Python, Django 6.0, Django Channels, Daphne
*   **Database**: PostgreSQL (Supabase)
*   **Frontend**: HTML, JavaScript, Tailwind CSS (CDN)
*   **AI**: Groq API (llama-3.3-70b-versatile)
*   **Infrastructure**: Google Cloud Run, Docker

## ローカル開発環境のセットアップ

### 前提条件

*   Python 3.12+
*   uv (パッケージマネージャー)

### 手順

1.  **リポジトリのクローン**
    ```bash
    git clone https://github.com/Yuji181181/cs4-test.git
    cd cs4-test
    ```

2.  **依存関係のインストール**
    ```bash
    uv sync
    ```

3.  **環境変数の設定**
    プロジェクトルートに `.env` ファイルを作成し、以下の内容を設定してください。
    ```text
    DATABASE_URL=your_supabase_postgres_url
    GROQ_API_KEY=your_groq_api_key
    ```

4.  **データベースのセットアップ**
    ```bash
    uv run python manage.py migrate
    ```

5.  **開発サーバーの起動**
    ```bash
    uv run python manage.py runserver
    ```
    ブラウザで `http://127.0.0.1:8000` にアクセスしてください。

## デプロイ (Google Cloud Run)

このプロジェクトは `Dockerfile` を含んでおり、Google Cloud Run へのデプロイに対応しています。

1.  **ビルド**
    ```bash
    gcloud builds submit --tag gcr.io/[PROJECT_ID]/slack-clone
    ```

2.  **デプロイ**
    ```bash
    gcloud run deploy slack-clone \
      --image gcr.io/[PROJECT_ID]/slack-clone \
      --platform managed \
      --region asia-northeast1 \
      --allow-unauthenticated \
      --timeout=3600 \
      --set-env-vars "GROQ_API_KEY=your_key,DATABASE_URL=your_db_url"
    ```

## 注意事項

*   セキュリティのため、`settings.py` の `DEBUG = True` は本番環境では `False` に変更することを推奨します。
*   AIチャット機能を使用するには、有効な Groq API Key が必要です。

## ライセンス

This project is for educational purposes.
