import pytz
import requests
from datetime import datetime
import os

# 以下个人内容全部放到仓库的secrets中（注意其中取值字段要跟自己的一致）

try:
    server_key = os.environ["key"]  # server酱key,登录之后就可使用
except:
    server_key = ""

try:
    username = os.environ["username"] # 自己的账号
    password = os.environ["password"] # 自己的密码
except:
    print("未获得完整用户名和密码")

s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",}
s.headers.update(header)


def login(s: requests.Session):
    sign_data = {
        "username": username,  # 自己的账号
        "password": password  # 自己的密码
    }
    r = s.post("https://itsapp.bjut.edu.cn/uc/wap/login/check", data=sign_data)

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

    if result.get('m') == "操作成功":
        print("打卡成功")
        if server_key != "":
            send_message(server_key, old['realname'] + result.get('m'), data)
    else:
        print("打卡失败，错误信息: ", result.get("m"))
        if server_key != "":
            send_message(server_key, old['realname'] + result.get('m'), data)

# 微信通知
def send_message(key, message, clock_info):
    send_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, message, clock_info)
    requests.get(send_url)


if __name__ == "__main__":

    #登录
    login(s)

    # 抓取昨天信息，用于今天提交
    yesterday_data = get_yesterday(s)

    # 提交
    submit(s, yesterday_data)
