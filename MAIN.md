# 要件：

大学の授業でこれを作成しています。プレゼンテーションのときに私が簡易的に動かせれば、その後は動かなくても良い
Djangoをメインで使用して、Slackのクローンをwebアプリケーションとして作成
Slackの全機能を作るのではなく、Chat機能などの主要な機能のみ実装する
最低限、ページからデータの登録と表示ができる
WebSocketを使用してリアルタイムでデータを表示する
ユーザー認証を導入する


# 技術スタック:

uv(管理用)
Django
Daphne
Channels
InMemoryChannelLayer
HTML
CSS
tailwindcss(CDN版)
JavaScript
WhiteNoise
supabase
Google Cloud Run(デプロイ用)


# 注意：
認証機能などは、できるだけDjangoの標準認証機能をそのまま使用するようにしてください。
環境変数は、.envファイルを使わずに、ファイルに直接記述してください。この授業が終わったら全て削除するので、セキュリティのことは考えなくて大丈夫です。
既にuvで環境を構築しています。また、最低限のDjangoの設定も構築済です。supabaseのURLもsettings.pyに記述しています。
しかし、supabaseとの接続はまだ試していません。