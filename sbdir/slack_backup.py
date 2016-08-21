#!/usr/bin/env python


import sys, os, requests, time, re, zipfile, argparse, smtplib
from sbdir.slack_time import SlackTime
from sbdir.send_mail import SendMail

HISTORY_LIST_URL='https://slack.com/api/channels.history'
CHANNEL_LIST_URL='https://slack.com/api/channels.list'
USER_LIST_URL='https://slack.com/api/users.list'

class SlackBackup(object):
    def __init__(self):
        ''' '''
        
        self.conf = {}

        self.st = SlackTime().now
        self.path = ''

        self.__version__ = '0.0.1'

        self.default_conf_path = './sbconf'
        self.conffile = self.default_conf_path

    def main(self, debug=False):
        """ make backup zip """
        # if dry-run option is true, debug option is true.
        self.debug = True if debug else False
        
        self.makeZip()
        self.rmFiles()

    def getConfig(self, path):
        """ get config file """
        confs = []
        with open(path) as conf:
            for line in conf:
                confs.append(re.sub('\n', '', line))

        for c in confs:
            conf_key, conf_value = c.split('=')[0], c.split('=')[1]
            self.conf[conf_key] = conf_value

        self.path = self.conf['ZIPPATH']
        self.users = self.getUser()
        self.channelIDs = self.getChannelsId()
        self.dirname = self.getDirName()
        
        self.confMail = {
                'froms': self.conf['FROMADDRESS'],
                'to': self.conf['TOADDRESS'],
                'cset': self.conf['CHARSET'],
                'subject': self.conf['SUBJECT'],
                'template': self.conf['TEMPLATE']
                }


    def makeBareConfig(self):
        """ make new confing file """
        temp = """
MYTOKEN=
OLDEST=
FROMADDRESS=
TOADDRESS=[]
ZIPPATH=
CHARSET=
SUBJECT=
TEMPLATE=
"""
        if os.path.exists(self.conffile):
            raise FileExistsError('sbconf is already exists.')

        new_conf = open(self.conffile, 'w')
        print(temp, file=new_conf)
        new_conf.close()
        return os.path.relpath(self.conffile)


    def isFiles(self):
        """ check out dir that attempt to make zip if .txt file is exist  """
        endswith = 'txt'
        files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith(endswith)] or False
        return files


    def makeZip(self):
        """ make archivedir zipfile"""
        if self.debug:
            myzip = zipfile.ZipFile(self.dirname + '.zip', 'w')
            myzip.close()
            print('slack_backup made {}.zip'.format(self.dirname))
            for ids in self.channelIDs:
                j = self.getJson(ids['id'])
                filename = self.getFileName(ids['name'])
                print(filename)
                
        else:
            with zipfile.ZipFile(self.dirname + '.zip', 'w') as myZip:
                for ids in self.channelIDs:
                    j = self.getJson(ids['id'])
                    filename = os.path.join(self.path, self.getFileName(ids['name']))
                    if 'messages' in j:
                        contents = self.formatMessage(j['messages'], self.users)
                    else:
                        contents = 'no messages found'
                    self.makeFile(filename, contents)
                    myZip.write(filename)


    def rmFiles(self):
        """ remove unnecesary files """
        files = self.isFiles()

        if isinstance(files, list):
            for f in files:
                os.remove(f)
        else:
            print('no files removed')


    def getDirName(self):
        dirname = '{}_{}_{}_{}_{}_backup'.format(self.st['year'], self.st['month'], self.st['day'], self.st['hour'], self.st['min'])
        return self.path + dirname;


    def getFileName(self, channel):
        ''' return filename with dateinfo '''
        return '{}_{}_{}_{}_{}_{}.txt'.format(channel, self.st['year'], self.st['month'], self.st['day'], self.st['hour'], self.st['min'])


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
        """ get all Channels ID """
        json = dict(requests.get(CHANNEL_LIST_URL, params={'token':self.conf['MYTOKEN']}).json())
        ids = [{'name':j['name'], 'id':j['id']} for j in json['channels']]
        return ids


    def makeFile(self, filename, contents):
        """ make new file """
        f = open(filename, 'a')
        print(contents, file=f)
        f.close()
 

    def getJson(self, channel):
        """ get json from slack """

        payload = {
                'token': self.conf['MYTOKEN'], 
                'latest': SlackTime().ts,
                'oldest': float(SlackTime().ts) - float(60 * 60 * 24 * int(self.conf['OLDEST'])),
                'channel': channel,
                'pretty':1,
                'count': 1000,
                }
        r = dict(requests.get(HISTORY_LIST_URL, params=payload).json())
        return r


    def getUser(self):
        """ get users list"""
        json =  dict(requests.get(USER_LIST_URL, params={'token':self.conf['MYTOKEN']}).json())
        uList = [{'id':j['id'], 'name':j['name']} for j in json['members']]
        return uList


    def mail(self):
        """ mail to configured address """
        mailer = SendMail(self.path, self.confMail, self.debug)
        mailer.send()



sb = SlackBackup()
