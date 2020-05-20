# -*- coding: utf-8 -*-

import xlwt
import time

# 创建一个工作簿，并设置编码
workbook = xlwt.Workbook(encoding='utf-8')
# 创建一个工作表
worksheet = workbook.add_sheet('汇率数据')


def write_excel(row, cloumn, value, styles=None):
    '''
    把数据写入 excel 表格中
    :param row: 行号
    :param cloumn: 列号
    :param value: 单元格值
    :param styles: 是否设置 style 样式
    :return:
    '''

    if styles != None:
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
        worksheet.write(row, cloumn, value, style)
    else:
        worksheet.write(row, cloumn, value)


def save(path):
    # 保存工作簿并命名
    workbook.save(path)


def date_string():
    '''
    获取当前时间的秒级
    :return: 返回 %Y-%m-%d %H:%M:%S 格式的字符串
    '''
    st = time.localtime(time.time())
    return time.strftime('%Y-%m-%d %H:%M:%S', st)


if __name__ == '__main__':
    write_excel(0, 0, '姓名')
    write_excel(0, 1, '年龄', '')
    # 设置保存 excel 的文件路径
    path = '/Users/jixuzhang/Desktop/data/' + date_string() + '.xls'
    save(path)
    print 'success'
