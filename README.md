# slack_backup
チーム内のオープンなチャンネルでのやりとりをバックアップします。
15/08/03 の時点でのAPIに対応して作ってあります。
slack-APIに変更があれば、対応予定です。

## インストール / 使い方 
1. `$ pip install slack_backup`

2. `$ slack_backup --init`
で未設定状態の設定ファイルを書き出してください。
以下のようなファイルが書き出されます。
```
MYTOKEN=
OLDEST=
FROMADDRESS=
TOADDRESS=[]
ZIPPATH=
CHARSET=
SUBJECT=
TEMPLATE=
```

3. 設定ファイルの記入をしたら
`$ slack_backup`
でバックアップzipを作成します。
`$ slack_backup --dry-run`
で作成予定バックアップと送信予定メール先を出力します。

4. 管理者にメールで送信する場合、
`$ slack_backup --mail`
をコマンドしてください。

5. 定期的なバックアップを取りたい場合、cronなどで設定してください。


## 依存関係
- requests
- pytz


## 動作環境
python 3.4〜
