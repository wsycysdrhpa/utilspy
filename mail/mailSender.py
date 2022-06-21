# -*- coding:utf-8 -*-


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import smtplib
import logging
import ConfigParser


class MailSender:
    def __init__(self, mail_config_path):
        logging.info("初始化ErrorMailSender...")
        self._loginInfo = {}
        #self._loadContactByConfigure()
        self._loadLoginInfoByConfigure(mail_config_path)
        self._infoList = []    # 要在邮件中添加的信息，字符串类型。
        self._errorList = []   # 要在邮件中添加的error，字符串类型。 Exception可以e.message来取得字符串描述
        self._title = "tvmao自动报告"   # 邮件的默认标题

    def setTitle(self, title):  #设置邮件标题
        self._title = title

    def addInfo(self, info):  #设置邮件内容
        self._infoList.append(info)

    def addError(self, error):
        self._errorList.append(error)

    def createMailAndSend(self):   # 生成邮件并发送
        content = ""
        for info in self._infoList:
            content += "INFO: %s \n" % info
        for error in self._errorList:
            content += "ERROR: %s \n" % error
        self.sendMail(self._title,content)
        self._reset()

    def sendMail(self,title="tvmao自动报告", errorMessage='', exception=None):   # 直接发送邮件
        if exception is not None:
            mailContent = errorMessage + exception.message
        else:
            mailContent = errorMessage
        try:
            self._sendSMTPMail(self._loginInfo, self._loginInfo["user"], self._loginInfo["receivers"],
                               title, mailContent)
            logging.info("已发送邮件，内容为：" + mailContent)
        except:
            logging.error("发送邮件失败。欲发送内容为：" + mailContent)

    def _reset(self):
        self._infoList = []
        self._errorList = []

    def _sendSMTPMail(self, loginInfo, fro, to, subject, text):
        """
        利用SMTP发送邮件到数个接受者。
        :param loginInfo: 登陆信息。dict类型。
        键为host user password 值示例：smtp.163.com  user1@163.com   xxxxx
        :param fro: 发送者，如 user1@163.com
        :param to: 接收者，list类型。如["jerry@qq.com", "tom@hotmail.com"]
        :param subject: 邮件主题，字符串类型。
        :param text: 邮件正文内容。
        """
        mailMessage = MIMEMultipart()
        mailMessage['From'] = fro
        mailMessage['Subject'] = subject
        mailMessage['To'] = COMMASPACE.join(to)
        mailMessage['Date'] = formatdate(localtime=True)
        mailMessage.attach(MIMEText(text, 'plain', 'utf-8'))
        #SMTP登录邮箱并发送邮件。
        smtp = smtplib.SMTP(loginInfo['host'])
        smtp.login(loginInfo['user'], loginInfo['password'])
        smtp.sendmail(fro, to, mailMessage.as_string())
        smtp.close()

    def _loadLoginInfoByConfigure(self, mail_conf_path):
        config = ConfigParser.ConfigParser()
        emailReceivers = []
        with open(mail_conf_path, "r") as configFile:
            config.readfp(configFile)
        emailReceiverInfo = config.get("mail", "mailReceivers")
        try:
            emailReceivers = emailReceiverInfo.rstrip().split(",")
        except:
            logging.error("从配置文件加载错误接收者发生错误")
        self._loginInfo = {"host": config.get("mail", "mailHost"),
                           "user": config.get("mail", "mailUser"),
                           "password": config.get("mail", "mailPassword"),
                           "receivers": emailReceivers}


if __name__ == "__main__":
    pass
