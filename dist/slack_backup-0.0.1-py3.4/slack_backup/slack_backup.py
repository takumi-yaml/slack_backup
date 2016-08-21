#!/usr/bin/env python


import sys, os, requests, time, re, zipfile, argparse, smtplib
from . import slackTime
from . import mail

MYTOKEN='xoxp-2834537761-2834937973-6600582150-b3bd09'
HISTORY_LIST_URL='https://slack.com/api/channels.history'
CHANNEL_LIST_URL='https://slack.com/api/channels.list'
USER_LIST_URL='https://slack.com/api/users.list'
OLDEST=7
FROMADDRESS='admin@localhost'
TOADDRESS=['rocca1141@gmail.com']
ZIPPATH='./zip/'

class SlackBackup(object):
    def __init__(self, urls, path):
        ''' '''

        parser = argparse.ArgumentParser(usage='%(prog)s', description='make backup zip file of your all channels and mail backup zip file')
        parser.add_argument('-m','--mail', action='store_true',  help='mail to zip file your account')
        parser.add_argument('-n','--notice', action='store_true',  help='only print files that you will make and zip')
        args = parser.parse_args()

        self.debug = False

        self.st = SlackTime().now
        self.path = path
        self.users = self.getUser()
        self.channelIDs = self.getChannelsId()
        self.dirname = self.getDirName()

        self.makeZip()
        self.rmFiles()

        if args.mail:
            self.mail()


    def isFiles(self):
        ''' jsonを用意するディレクトリにjsonが無いかどうかチェック '''
        endswith = '{}_{}_{}'.format(self.st['year'], self.st['month'], self.st['day'])
        files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith(endswith)] or False
        return files

    def makeZip(self):
        ''' make archivedir zipfile'''
        if self.debug:
            print('I made {}.zip'.format(self.dirname))
            for ids in self.channelIDs:
                j = self.getJson(ids['id'])
                filename = self.getFileName(ids['name'])
                contents = self.formatMessage(j['messages'], self.users)
                print(filename)
        else:
            with zipfile.ZipFile(self.dirname + '.zip', 'w') as myZip:
                for ids in self.channelIDs:
                    j = self.getJson(ids['id'])
                    filename = os.path.join(self.path, self.getFileName(ids['name']))
                    contents = self.formatMessage(j['messages'], self.users)
                    self.makeFile(filename, contents)
                    myZip.write(filename)

    def rmFiles(self):
        ''' remove unnecesary files '''
        files = self.isFiles()

        if isinstance(files, list):
            for f in files:
                if self.debug:
                    print('remove {}'.format(f))
                else:
                    os.remove(f)
        else:
            print('no files removed')
            return


    def getDirName(self):
        st = SlackTime().now
        dirname = '{}_{}_{}_backup'.format(st['year'], st['month'], st['day'])

        return self.path + dirname;

    def getFileName(self, channel):
        ''' return filename with dateinfo '''
        return '{}_{}_{}_{}'.format(channel, self.st['year'], self.st['month'], self.st['day'])

    def formatMessage(self, messages, userList):
        ''' set messages messagesFormat '''

        contents = ''

        for m in messages:
            username = ''
            t = time.strftime( '%Y-%m-%d %H:%M', time.localtime(int(m['ts'].split('.')[0])))
            text = ''

            for u in userList:
                if 'user' in m:
                    if u['id'] == m['user']:
                        username = u['name']
                elif 'bot_id' in m:
                    username = m['bot_id']

                if '<@' in m['text']:
                    uids = re.findall(r"<@(\w{9}).*?>", m['text'])
                    for uid in uids:
                        if u['id'] == uid:
                            text = m['text'].replace(uid, u['name'])

            else:
                if not username:
                   username = 'UNKNOWN'
                if not text:
                   text = m['text']

            contents += "{name} : {time} : {message}\n\n".format(name=username, time=t, message=text)

        return contents;


    def getChannelsId(self):
        ''' get all Channels ID '''
        json = dict(requests.get(CHANNEL_LIST_URL, params={'token':MYTOKEN}).json())
        ids = [{'name':j['name'], 'id':j['id']} for j in json['channels']]
        return ids

    def makeFile(self, filename, contents):
        ''' ファイル作成のモデル '''
        f = open(filename, 'a')
        print(contents, file=f)
        f.close()
        
    def getJson(self, channel):
        ''' historyのjsonを取りに行く '''
        payload = {
                'token':MYTOKEN, 
                'latest': SlackTime().ts,
                'oldest': float(SlackTime().ts) - float(60 * 60 * 24 * OLDEST),
                'channel': channel,
                'pretty':1,
                'count': 1000,
                }
        r = dict(requests.get(HISTORY_LIST_URL, params=payload).json())
        return r

    def getUser(self):
        ''' get users list'''
        json =  dict(requests.get(USER_LIST_URL, params={'token':MYTOKEN}).json())
        uList = [{'id':j['id'], 'name':j['name']} for j in json['members']]
        return uList


    def mail(self):
        mailer = sendMail(self.path)
        mailer.send()



def main():
    sb = SlackBackup('urls', './zips/')

if __name__ == "__main__":
    main()


