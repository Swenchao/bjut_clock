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

    data = {
        'ismoved': old['ismoved'],
        'jhfjrq': old['jhfjrq'],
        'jhfjjtgj': old['jhfjjtgj'],
        'jhfjhbcc': old['jhfjhbcc'],
        'sftjzgfxdq': old['sftjzgfxdq'],
        'dqszyqfxdj': old['dqszyqfxdj'],
        'tw': old['tw'],
        'sfcxtz': old['sfcxtz'],
        'sfjcbh': old['sfjcbh'],
        'sfcxzysx': old['sfcxzysx'],
        'qksm': old['qksm'],
        'sfyyjc': old['sfyyjc'],
        'jcjgqr': old['jcjgqr'],
        'remark': old['remark'],
        'address': old['address'],
        'geo_api_info': old['geo_api_info'],
        'area': old['area'],
        'province': old['province'],
        'city': old['city'],
        'sfzx': old['sfzx'],
        'sfjcwhry': old['sfjcwhry'],
        'sfjchbry': old['sfjchbry'],
        'sfcyglq': old['sfcyglq'],
        'gllx': old['gllx'],
        'glksrq': old['glksrq'],
        'jcbhlx': old['jcbhlx'],
        'jcbhrq': old['jcbhrq'],
        'bztcyy': old['bztcyy'],
        'sftjhb': old['sftjhb'],
        'sftjwh': old['sftjwh'],
        'sfsfbh': old['sfsfbh'],
        'xjzd': old['xjzd'],
        'jcwhryfs': old['jcwhryfs'],
        'jchbryfs': old['jchbryfs'],
        'szgj': old['szgj'],
        'dqjzzt': old['dqjzzt'],
        'ljrq': old['ljrq'],
        'ljjtgj': old['ljjtgj'],
        'ljhbcc': old['ljhbcc'],
        'fjrq': old['fjrq'],
        'fjjtgj': old['fjjtgj'],
        'fjhbcc': old['fjhbcc'],
        'fjqszgj': old['fjqszgj'],
        'fjq_province': old['fjq_province'],
        'fjq_city': old['fjq_city'],
        'fjq_szdz': old['fjq_szdz'],
        'jrfjjtgj': old['jrfjjtgj'],
        'jrfjhbcc': old['jrfjhbcc'],
        'fjyy': old['fjyy'],
        'szsqsfty': old['szsqsfty'],
        'sfxxxbb': old['sfxxxbb'],
        'jcjg': old['jcjg'],
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y%m%d"),
        'uid': old['uid'],
        'created': old['created'],
        'id': old['id'],
        'gwszdd': '',
        'sfyqjzgc': '',
        'jcqzrq': old['jcqzrq'],
        'sfjcqz': old['sfjcqz'],
        'jrsfqzys': '',
        'jrsfqzfy': '',
        'szsqsfybl': old['szsqsfybl'],
        'sfsqhzjkk': old['sfsqhzjkk'],
        'sqhzjkkys': old['sqhzjkkys'],
        'sfygtjzzfj': old['sfygtjzzfj'],
        'gtjzzfjsj': old['gtjzzfjsj']
    }

    r = s.post("https://itsapp.bjut.edu.cn/ncov/wap/default/save", data=data)

    result = r.json()
    # print(result)

    if result.get('m') == "操作成功":
        # print("打卡成功")
        if server_key != "":
            send_message(server_key, old['realname'] + result.get('m'), data)
    else:
        # print("打卡失败，错误信息: ", result.get("m"))
        if server_key != "":
            send_message(server_key, old['realname'] + result.get('m'), data)


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