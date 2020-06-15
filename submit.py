import pytz
import requests
from datetime import datetime


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
    # print(daily)
    json_data = data.json()
    # 其中昨天数据存放于json的d中，拿不到则为 None
    d = json_data.get('d', None)
    if d:
        return data.json()['d']
    else:
        print("未获取到昨天信息")
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
        'old_szdd': old['szdd'],
        'sfyyjc': old['sfyyjc'],
        'app_id': 'bjut'
    }
    r = s.post("https://itsapp.bjut.edu.cn/ncov/wap/default/save", data=new_daily)

    print("提交信息:", new_daily)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))


if __name__ == "__main__":

    #登录
    login(s)

    # 抓取昨天信息，用于今天提交
    yesterday_data = get_yesterday(s)

    # 提交
    submit(s, yesterday_data)
