# -*- coding: utf-8 -*-

import requests
import json


# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


def querySolr():
    url = ''
    body = {"table": "others_rpt_contacts", "q": "_id:576b5bd818ca47052cdfefea", "start": "0", "rows": "1",
            "sort": "_id,rpt_ut", "unit": "desc", "fl": "", "cursorMark": "*"}
    headers = {'content-type': "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    json_data = response.json()
    real_data = json_data['result']['result']
    ctc_lts = real_data[0]['ctc_lt'].encode("utf-8")
    # print type(ctc_lts), ctc_lts
    list_json = json.loads(ctc_lts[1: -1])
    # print type(list_json)
    for ctc_lt in list_json:
        print ctc_lt['ctc_ph_mk']


def querySolr1():
    url = ''
    body = {"table": "rpt_contacts", "q": "tk:d6976eb1015a4c4abbe90d4ab2bf34fb", "start": "0", "rows": "1",
            "sort": "_id,rpt_ut", "unit": "desc", "fl": "", "cursorMark": "*"}
    headers = {'content-type': "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    json_data = response.json()
    real_data = json_data['result']['result']
    ctc_lts = real_data[0]['ctc_lt'].encode("utf-8")
    # print type(ctc_lts), ctc_lts
    list_json = json.loads(ctc_lts[1: -1])
    # print type(list_json)
    for ctc_lt in list_json:
        print ctc_lt['ctc_ph_mk']


if __name__ == '__main__':
    # querySolr1()
    querySolr1()
