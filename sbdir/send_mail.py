import smtplib, datetime, os
from email.mime.text import MIMEText
from email.header import Header
from email import charset
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders


class SendMail(object):
    def __init__(self, path, confDict, debug=False):
        ''' mail to specified account '''
        
        self.debug = True if debug else False

        self.mailFrom = confDict['froms']
        self.mailTo = confDict['to'][1:-1].replace('\'', '').split(',')
        self.cset = confDict['cset']
        self.subject = confDict['subject']
        self.template = confDict['template']
        self.path = path

        self.message = MIMEMultipart()
        self.message['Subject'] = Header(self.subject, self.cset)
        self.message['From']    = self.mailFrom
        self.message['To']      = ", ".join(self.mailTo)
        self.message.attach(MIMEText(self.setUpMsg(), 'plain', self.cset))

    def send(self):
        """ send mail. if option dry-run is true, only print mailFrom, mailTo, message """

        files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith('zip')] or False

        # set 'filename' to latest zip
        filenames = [filename.split('_') for filename in files]
        sorted(filenames, key=lambda x: ''.join(x[1:-1]))

        filename = '_'.join(filenames[-1])
        part = MIMEBase('application', "zip")
        part.set_payload( open(filename, 'rb').read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(filename)))
        self.message.attach(part)

        if self.debug:
            info = """
            mailFrom is {}
            mailTo is {}
            message is:\n{}
"""
            print(info.format(self.mailFrom, self.mailTo, self.message.as_string()))

        else:
            p = smtplib.SMTP_PORT
            server = smtplib.SMTP('localhost', p)
            server.sendmail(self.mailFrom, self.mailTo, self.message.as_string())
            server.quit()

    def setUpMsg(self):
        """ set message with create date """
        d = datetime.date.today()
        d = d.strftime("%Y/%m/%d %h:%M")
        
        msg = self.template
        msg += '\n{}'.format(d)
        return msg
