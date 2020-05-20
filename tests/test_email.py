# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from conf import email_conf


def test_email(subject_content, content, receiver, path=None):
    '''
    测试发送邮件
    :param subject_content: 邮件主题
    :param content: 邮件正文内容
    :param receiver: 收件人
    :param path: 附件地址 可选项
    :return:
    '''
    try:
        # 设置服务器
        mail_host = email_conf.mail_host
        # 用户名
        mail_user = email_conf.mail_user
        # 密码
        mail_pass = email_conf.mail_pass
        # 发件人地址
        sender = email_conf.sender
        # 邮件主题
        subject = subject_content
        # 主题包含中文时
        subject = Header(subject, 'utf-8').encode()
        # 构造邮件对象MIMEMultipart对象
        # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        msg['To'] = ";".join(receiver)
        # 构造文字内容
        text = content
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)
        if path != None:
            # 构造附件
            sendfile = open(path, 'rb').read()
            text_att = MIMEText(sendfile, 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            # 以下附件可以重命名成 20181107154552.xls
            text_att["Content-Disposition"] = 'attachment; filename="汇率.xls"'
            msg.attach(text_att)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(mail_host)
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, receiver, msg.as_string())

    except Exception as e:
        print 'email exception ' + str(e)
    finally:
        smtp.quit()


if __name__ == '__main__':
    # 收件人地址
    receiver = email_conf.receiver
    # 邮件正文
    content = 'python'
    # 邮件主题
    subject = 'test'
    # 附件地址
    # path = '/Users/jixuzhang/Desktop/data/20181107154552.xls'
    test_email(subject, content, receiver)
    print 'success'
