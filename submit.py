import pytz
import requests
from datetime import datetime

server_key = ""  # server酱key,登录之后就可使用

s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",}
s.headers.update(header)


def login(s: requests.Session):
    payload = {
        "username": "",  # 自己的账号
        "password": ""  # 自己的密码
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
        print("未获取到昨天信息")
        exit(1)


def submit(s: requests.Session, old: dict):
    r = s.post("https://itsapp.bjut.edu.cn/ncov/wap/default/save", data=old)
    result = r.json()
    # print(result)

    if result.get('m') == "操作成功":
        print("打卡成功")
        if server_key != "":
            send_message(server_key, result.get('m'), old)
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))
        if server_key != "":
            send_message(server_key, old['realname'] + result.get('m'), old)


# 微信通知
def send_message(key, message, clock_info):
    send_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, message, clock_info)
    requests.get(send_url)


if __name__ == "__main__":

    #登录
    login(s)

    # 抓取昨天信息，用于今天提交
    yesterday_data = get_yesterday(s)
    # print(yesterday_data)
    # 提交
    submit(s, yesterday_data)
