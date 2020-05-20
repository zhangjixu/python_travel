# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import xlwt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from conf import email_conf

URL = 'http://www.boc.cn/sourcedb/whpj/'
# 定义全局变量 row
row = 0
# 定义全局变量 tuple_list
tuple_list = []


def get_page_no():
    '''
    获取最大页面数
    :return:
    '''
    url = 'http://www.boc.cn/sourcedb/whpj/index.html'
    # 发送 http get 请求
    res = requests.get(url)
    res.encoding = 'utf-8'
    content = res.text
    # print content
    # 创建 beautifulsoup 对象并使用 html 解析器
    soup = BeautifulSoup(content, 'html.parser')
    turn_page = soup.find('div', attrs={'class': 'turn_page'})
    return turn_page.p.span.get_text()


def parse_html(content, page_index):
    '''
    解析网页
    :param content: requests 请求后返回的 response 内容
    :param page_index: 第 page_index 页
    :return:
    '''
    global row
    global tuple_list
    try:
        # 创建 beautifulsoup 对象并使用 html 解析器
        soup = BeautifulSoup(content, 'html.parser')
        # 获取所有 tr 的标签，排除第一个和最后两个
        list_tr = soup.find_all('tr')[1:-2]
        # 第一个 tr 标签是标题内容
        if page_index == 0:
            list_th = list_tr[0].find_all('th')
            for th_index, th_item in enumerate(list_th):
                tuple_list.append((row, th_index, th_item.get_text()))
            # 每次遍历一个对 row 进行加一操作
            row += 1

        # 以下都是 td 标签
        for list_td in list_tr[1:]:
            for td_index, td_item in enumerate(list_td.find_all('td')):
                tuple_list.append((row, td_index, td_item.get_text()))

            row += 1
    except Exception as e:
        print 'parse_html exception: ' + str(e)


def write_excel():
    '''
    把数据写入 excel 表格中
    :return:
    '''
    # 创建一个工作簿，并设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个工作表
    worksheet = workbook.add_sheet('汇率数据')
    try:
        tuple_list_1 = tuple_list[0:8]
        tuple_list_2 = tuple_list[8:]
        # 把标题写入 excel 文件中并设置样式
        for tup_1 in tuple_list_1:
            # 初始化样式
            style = xlwt.XFStyle()
            # 为样式创建字体
            font = xlwt.Font()
            # 设置字体为加粗
            font.bold = True
            # 将该 font 设定为 style 的字体
            style.font = font
            # 初始化居中方式
            alignment = xlwt.Alignment()
            # 垂直居中
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            # 将该居中方式应用于 style 的居中方式
            style.alignment = alignment
            worksheet.write(tup_1[0], tup_1[1], tup_1[2], style)

        # 把具体的汇率信息写入 excel 文件中
        for tup_2 in tuple_list_2:
            worksheet.write(tup_2[0], tup_2[1], tup_2[2])

        path = '/Users/jixuzhang/Desktop/data/' + date_string() + '.xls'
        workbook.save(path)
    except Exception as e:
        print 'write_excel exception: ' + str(e)


def date_string():
    '''
    获取当前时间的秒级
    :return: 返回 %Y-%m-%d %H:%M:%S 格式的字符串
    '''
    st = time.localtime(time.time())
    return time.strftime('%Y-%m-%d %H:%M:%S', st)


def crawl_bank():
    '''
    抓取中国银行汇率数据
    :return:
    '''
    global row
    global tuple_list
    # 每次调用 crawl_bank() 函数，重置 row = 0
    row = 0
    # 每次调用 crawl_bank() 函数，把列表 tuple_list 清空
    tuple_list = []
    # 获取最大页面数
    page_no = get_page_no()
    for i in range(0, int(page_no)):
        if i == 0:
            url = URL + 'index.html'
        else:
            url = URL + 'index_' + str(i) + '.html'

        # 伪装浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        # 发送 http get 请求
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        # 获取 http 请求响应数据
        content = res.text
        parse_html(content, i)

    # 把数据写入 excel 中
    write_excel()


def send_email(subject_content, content, receiver, path=None):
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
        print 'send_email exception %s' % (e)
    finally:
        smtp.quit()


if __name__ == '__main__':
    # 收件人地址
    receiver = email_conf.receiver
    # 邮件正文
    content = '汇率信息抓取完成'
    # 邮件主题
    subject = '汇率信息'
    # 12 分钟的秒数
    period = 60 * 12
    # period = 3
    while True:
        crawl_bank()
        # 发送邮件
        send_email(subject, content, receiver)
        print 'success'
        # 每隔 12 分钟后重新抓取一次
        time.sleep(period)
