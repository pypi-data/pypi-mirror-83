import poplib
import imaplib
import smtplib
import chardet
import os
from email.mime.text import MIMEText
from email.header import Header
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from loguru import logger

class SimpleEmail:

    def __init__(self, host, port, user, pass_):
        self.host = host
        self.port = int(port)
        self.user = user
        self.pass_ = pass_

    def loging_POP3(self):
        try:
            server = poplib.POP3(self.host, self.port)
            server.user(self.user)
            server.pass_(self.pass_)
            return GetEmail(server)
        except BaseException as e:
            logger.error(f'邮件登录报错 {e}')
            logger.exception(e)
            raise Exception('连接邮箱报错')

    def loging_POP3_SSL(self):
        try:
            server = poplib.POP3_SSL(self.host, self.port)
            server.user(self.user)
            server.pass_(self.pass_)
            return server
        except BaseException as e:
            logger.error(f'邮件登录报错 {e}')
            logger.exception(e)
            raise Exception('连接邮箱报错')

    def loging_IMAP4(self):
        try:
            server = imaplib.IMAP4(host=self.host, port=self.port)
            server.login(self.user, self.pass_)
            result = server.select('INBOX')
            return server
        except BaseException as e:
            logger.error(f'邮件登录报错 {e}')
            logger.exception(e)
            raise Exception('连接邮箱报错')

    def loging_IMAP4_SSL(self):
        try:
            server = imaplib.IMAP4_SSL(host=self.host, port=self.port)
            server.login(self.user, self.pass_)
            result = server.select('INBOX')
            return server
        except BaseException as e:
            logger.error(f'邮件登录报错 {e}')
            logger.exception(e)
            raise Exception('连接邮箱报错')

class SenEmail(SimpleEmail):

    def send_email(self, title=None, body=None, attachment=[], sender=None, to=[], cc=[]):
        '''
        发送邮件,带附件
        :param title: 主题
        :param body: 正文
        :param attachment:附件路径
        :param sender: 发件人
        :param to: 收件人
        :param cc: 抄送人
        :return:
        '''

        '''
        发送附件对象;
        使用MIMEMultipart来标示这个邮件是多个部分组成的，然后attach各个部分。如果是附件，则add_header加入附件的声明。
        MIME有很多种类型，这个略麻烦，如果附件是图片格式，我要用MIMEImage，如果是音频，要用MIMEAudio，如果是word、excel，我都不知道该用哪种MIME类型了，得上google去查。
        最懒的方法就是，不管什么类型的附件，都用MIMEApplication，MIMEApplication默认子类型是application/octet-stream。
        '''
        # 添加对象
        message = MIMEMultipart()
        # 发送附件对象
        apart = None
        if attachment:
            for fpath in attachment:
                try:
                    fname = fpath.split("\\")[-1]
                    logger.info(f'{fpath} {fname}')
                    apart = MIMEApplication(open(fpath, 'rb').read())
                    apart.add_header('Content-Disposition', 'attachment', filename=f'{fname}')
                    message.attach(apart)
                except BaseException as e:
                    logger.error(f'加载附件报错:{e}')
        # 发送文本对象
        # strApart = MIMEText(body, 'plain', 'utf-8')
        strApart = MIMEText(body, 'html', 'utf-8')
        if strApart:
            message.attach(strApart)
        if cc:
            message['Cc'] = ';'.join(cc)
        if to:
            message['To'] = ';'.join(to)  # 邮件上显示的收件人,如果是多人,需要将 list转 string
        message['Subject'] = Header(title, 'utf-8')  # 邮件主题
        message['From'] = sender  # 邮件上显示的发件人
        try:
            smtp = smtplib.SMTP()  # 创建一个连接
            smtp.connect(self.host)  # 连接发送邮件的服务器
            smtp.login(self.user, self.pass_)  # 登录服务器
            smtp.sendmail(sender, to+cc, message.as_string())  # 填入邮件的相关信息并发送
            logger.info("邮件发送成功!!!")
            smtp.quit()
        except BaseException as e:
            logger.error(e)
            logger.error('邮件发送失败.')

class GetEmail():

    def __init__(self, server):
        self.server = server

    def decode_str(self, s):
        ''''''
        value, charset = decode_header(s)[0]
        if charset:
            if charset == 'gb2312':
                charset = 'gb18030'
            value = value.decode(charset)
        return value

    def decode_e_mail(self, data):
        '''解析转码邮件内容'''
        try:
            return data.decode('utf-8')
        except:
            try:
                return data.decode('gbk')
            except Exception as e:
                try:
                    return data.decode('gb18030', 'ignore')
                except:
                    logger.error(chardet.detect(data))
                    logger.error(f'解析转码错误类型是 {e.__class__.__name__}')
                    logger.exception(f'解析转码错误明细是 {e}')
                    logger.error(e.__traceback__.tb_lineno)
        return None

    def get_email_headers(self, msg):
        '''构造邮件头'''
        headers = {}
        for header in ['From', 'Subject', 'Date']:
            value = msg.get(header, '')
            if value:
                if header == 'Date':
                    headers['Date'] = value
                if header == 'Subject':
                    subject = self.decode_str(value)
                    headers['Subject'] = subject
                if header == 'From':
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(hdr)
                    from_addr = u'%s <%s>' % (name, addr)
                    headers['From'] = from_addr
        return headers

    def get_email_content(self, message, savepath):  # 下载附件函数
        '''
        邮件附件下载
        :param message: message object
        :param savepath: 附件保存路径
        :return:
        '''
        file_name_list = []
        for part in message.walk():
            download_filename = part.get_filename()
            if download_filename:
                download_filename = self.decode_str(download_filename)
                print(f'附件名称:{download_filename}', savepath)
                data = part.get_payload(decode=True)
                abs_filename = os.path.join(savepath, download_filename)
                try:
                    print(f'邮件附件解压地址: {abs_filename}')
                    attach = open(abs_filename, 'wb')
                    attach.write(data)
                    attach.close()
                    file_name_list.append(download_filename)
                except BaseException as e:
                    print(f'附件下载错误 {abs_filename}')
                    print(e)
        return str(file_name_list)


if __name__ == '__main__':
    host = 'xx.xx.xx.xx'
    port = 110
    user = ''
    pass_ = ''
    s = SenEmail(host=host, port=port, user=user, pass_=pass_)

    title = ''
    body = ''
    attachment = ['']
    sender = ''
    to = ['']
    cc = []
    s.send_email(title=title, body=body, attachment=attachment, sender=sender, to=to, cc=cc)