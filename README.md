# Tech Forward

wikiアプリです。

## 概要

技術共有システム

## ローカル起動

この README があるディレクトリで実行します。Docker Compose と Python 3 が必要です。
Nuxt 2、Flask、MariaDB、Memcached、Nginx を起動します。
DB 接続情報は `.env.sample` を基に設定します。DB のパスワードは
`.secrets/db_pass.txt` に保存し、Docker の secret として渡します。

```bash
cp .env.sample .env
mkdir -p .secrets
chmod 700 .secrets
python3 -c 'import secrets; print(secrets.token_hex(24))' \
  > .secrets/db_pass.txt
chmod 644 .secrets/db_pass.txt
docker compose up --build -d
```

ブラウザで `http://localhost:8080` を開き、新規登録から利用します。
secret の親ディレクトリは所有者だけがアクセスできるように保ちます。
ファイル自体はコンテナ内の非 root ユーザーが読み取れる必要があります。
`HTTP_PORT` で公開ポートを変更できます。公開先はループバックに限定しています。

DB データは名前付きボリューム `dbData` に保存されます。
アプリの再起動では削除もテストデータ投入も行いません。
固定パスワードの初期アカウントは作成しません。

このディレクトリで、停止する場合は次を実行します。DB データは保持します。

```bash
docker compose down
```
