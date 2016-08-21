#!/usr/bin/env python


from datetime import datetime
import time, pytz, os

class SlackTime:
    '''python環境のタイムゾーンの設定と時間関連の処理'''
    def __init__(self):
        # 環境変数を変更
        os.environ['TZ'] = 'JST'
        time.tzset()
        japan_time = datetime.now(pytz.timezone('Asia/Tokyo'))

        # ファイル名
        timeNow = str(japan_time).split(' ')[0].split('-')
        timeNow_h = str(japan_time).split(' ')[1].split('.')[0].split(':')
        self.now = {
            'year':     timeNow[0],
            'month':    timeNow[1],
            'day':      timeNow[2],
            'hour':     timeNow_h[0],
            'min':      timeNow_h[1],
                }
        # バックアップ取得用のUTCタイムスタンプ
        self.ts = str(time.time()).split('.')[0]


