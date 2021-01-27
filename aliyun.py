# -*- coding: utf8 -*-

import pytz
import requests
from datetime import datetime


s = requests.Session()

server_key = ""  # server酱 key（不填无所谓，只不过无法收到通知）


def login(s: requests.Session):
    payload = {
        "username": "",  # 个人账号
        "password": ""  # 个人密码
    }
    r = s.post("https://itsapp.bjut.edu.cn/uc/wap/login/check", data=payload)

    if r.json().get('m') != "操作成功":
        print(r.text)
        print("登录失败")
        exit(1)


def get_yesterday(s: requests.Session):
    data = s.get("https://itsapp.bjut.edu.cn/ncov/api/default/daily?xgh=0&app_id=bjut")
    json_data = data.json()

    # 其中昨天数据存放于json的d中，拿不到则为 None
    d = json_data.get('d', None)
    if d:
        return data.json()['d']
    else:
        exit(1)


def submit(s: requests.Session, old: dict):

    r = s.post("https://itsapp.bjut.edu.cn/ncov/wap/default/save", data=old)

    result = r.json()
    if result.get('m') == "操作成功":
        if server_key != "":
            send_message(server_key, result.get('m'), old)
    else:
        if server_key != "":
            send_message(server_key, result.get('m'), old)


# 微信通知
def send_message(key, title, body):
    msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
    requests.get(msg_url)


# 阿里云函数入口
def handler(event, context):

    # 登录
    login(s)

    # 抓取昨天信息，用于今天提交
    yesterday_data = get_yesterday(s)

    # 提交
    submit(s, yesterday_data)

