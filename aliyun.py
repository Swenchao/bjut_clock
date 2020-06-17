# -*- coding: utf8 -*-

import pytz
import requests
from datetime import datetime


s = requests.Session()

server_key = ""  # server酱 key（不填无所谓，只不过无法收到通知）


def login(s: requests.Session, username, password):
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
    new_daily = {
        # 设置时区，获取时间（服务器未必在国内）
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
        'realname': old['realname'],
        'number': old['number'],
        'sfzx': old['sfzx'],  # 在校
        'sfzgn': '1',  # 所在地点（1：大陆）
        # 'szdd': old['szdd'],  # 所在地点
        'area': old['area'],  # 定位
        'dqjzzt': old['dqjzzt'],  # 居住状态
        # 'dqjzzt':'6',
        'tw': old['tw'],  # 体温
        'sftjwh': old['sftjwh'],  # 经停武汉
        'sftjhb': old['sftjhb'],  # 经停湖北除武汉
        'sfcyglq': old['sfcyglq'],  # 观察期
        # 'bztcyy': old['bztcyy'],  # 情况
        'sfjcwhry': old['sfjcwhry'],  # 接触过其他到武汉的人
        # 'jhfjsftjwh': old['jhfjsftjwh'],  # 接触过其他到武汉的人
        'sfjchbry': old['sfjchbry'],  # 接触过其他到湖北的人
        # 'jhfjsftjhb': old['jhfjsftjhb'],  # 接触过其他到湖北的人
        'geo_api_info': old['old_city'],  # 定位信息
        'jcjgqr': old['jcjgqr'],  # 属于以下哪种情况
        'sfcxtz': old['sfcxtz'],  # 是否出现乏力..情况
        'sfjcbh': old['sfjcbh'],  # 是否接触疑似人员
        'sfcxzysx': old['sfcxzysx'],  # 值得注意情况
        'ismoved': old['ismoved'],  # 判断位置是否变化

        # 未解析（其中有定位信息）
        'address': old['address'],
        'province': old['province'],
        'city': old['city'],
        'old_city': old['old_city'],
        'geo_api_infot': old['geo_api_infot'],  # 可能为定位信息
        'sfyyjc': old['sfyyjc'],
        'app_id': 'bjut'
    }
    r = s.post("https://itsapp.bjut.edu.cn/ncov/wap/default/save", data=new_daily)

    result = r.json()
    if result.get('m') == "操作成功":
        if server_key != "":
            send_message(server_key, result.get('m'), new_daily)
    else:
        if server_key != "":
            send_message(server_key, result.get('m'), new_daily)



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

