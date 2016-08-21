=============
Slack_backup
=============

About
=====

チーム内のオープンなチャンネルでのやりとりをバックアップします。
15/08/03 の時点でのAPIに対応して作ってあります。
slack-APIに変更があれば、対応予定です。

Backup messages in your team of all open channels.
We use slack API in 
If slack API is changed, we take care of this.

Usage
========

1. Install

.. code-block:: bash

  $ pip install slack_backup


2. Initialize
   make your config file.

.. code-block:: bash

  $ slack_backup --init

で未設定状態の設定ファイルを書き出してください。
以下のようなファイルが書き出されます。

::

  MYTOKEN=
  OLDEST=
  FROMADDRESS=
  TOADDRESS=[]
  ZIPPATH=
  CHARSET=
  SUBJECT=
  TEMPLATE=


3. Only backup. Just make zip.
   設定ファイルの記入をし、パスを渡すとバックアップzipを作成します。

.. code-block:: bash

  $ slack_backup ./sbconf

If you want to know how this module works, don't want to make backup, use *dry-run* option.
  
  dry-runオプションで作成予定バックアップと送信予定メール先を出力します。

.. code-block:: bash

  $ slack_backup --dry-run


If you want to mail backup zip file,  use *mail* option.

mailオプションで管理者にメールします。

.. code-block:: bash

  $ slack_backup --mail / -m


4. 定期的なバックアップを取りたい場合、cronなどで設定してください。
   If you want to backup regularity,  use *cron* or like that.

dependencies
============

- requests
- pytz


dependencies
============

- requests
- pytz

license
============

- requests
- pytz


