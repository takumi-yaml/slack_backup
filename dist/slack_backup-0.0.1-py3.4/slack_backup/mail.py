import smtplib, datetime, os
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

FROMADDRESS='admin@localhost'
TOADDRESS=['rocca1141@gmail.com']
SUBJECT='メールテスト'
CHARSET='iso-2022-jp'
TEMPLATE= '''
        {y}/{m}/{d}
'''

class sendMail(object):
    def __init__(self, path):
        ''' mail to specified account '''
        self.mailFrom = FROMADDRESS
        self.mailTo = TOADDRESS
        self.cset = CHARSET
        self.subject = SUBJECT
        self.template = TEMPLATE
        self.path = path

        self.message = MIMEMultipart()
        self.message['Subject'] = Header(self.subject, self.cset)
        self.message['From']    = self.mailFrom
        self.message['To']      = ", ".join(self.mailTo)
        self.message.attach(MIMEText(self.setUpMsg(), 'plain', self.cset))

    def send(self):
        files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith('zip')] or False

        for filename in files:
            part = MIMEBase('application', "zip")
            part.set_payload( open(filename, 'rb').read() )
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(filename)))
            self.message.attach(part)

        p = smtplib.SMTP_PORT
        server = smtplib.SMTP('localhost', p)
        server.set_debuglevel(1)
        server.sendmail(self.mailFrom, self.mailTo, self.message.as_string())
        server.quit()

    def setUpMsg(self):
        d = datetime.date.today()
        d = d.strftime("%Y/%m/%d").split('/')
        
        msg = self.template.format(y=d[0], m=d[1], d=d[2])
        return msg
