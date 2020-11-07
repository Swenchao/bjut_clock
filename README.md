# 注：编写此脚本目的是技术应用探索，大家请根据自己生活实际情况合理使用。请一切听从学校组织安排，不要存在侥幸，瞒报自己真实情况妨碍疫情防护，危害他人生命健康。

脚本有什么问题可发送邮件，进行询问：scwrite678@outlook.com

学校不再要求每天打卡，可修改action的配置文件（https://github.com/Swenchao/bjut_clock/blob/master/.github/workflows/main.yml）将其中5 6行定时注释掉即可。

# bjut_clock

北工大疫情自动打卡脚本（北京工业大学  疫情）
不需要服务器也可用，git action以及云函数版本都可用

## 脚本三部分

### 自动登录

只需要将其中username和password修改成自己的就可以了

### 获取昨天数据

其中获得的数据是个json串的
    {
        e:0
        m:"操作成功"
        d:{
        ...
        }
    }
其中要提交的数据都在 d 中。将其解析返回。

### 对数据进行包装提交

剩下的就是重新进行封装提交了

## 注：若是北工大的，只需要改下登录那块账号密码就可以使用了

其中可能还有输入的，放到服务器改成日志就可以了~

亲，如果满意，点星好评哦~


## 更新内容

1. 新增打卡微信通知，需要有Server酱的key，只需要登录就能获得一个key，放到脚本里面就可使用了~

Server酱网站：http://sc.ftqq.com/3.version

2. 新增阿里云函数脚本代码（在源代码基础上略微修改（函数入口变化））——aliyun.py

阿里云开通云函数，新建函数-->事件函数(运行环境选择python3)-->完成-->代码执行部分（index.py清空 粘贴 aliyun.py代码）-->触发器（创建触发器-->定时触发器）-->完结

**注：** 最大时间延迟修改之前3s改成5s或10s，不然会超时


3. 新增git action打卡脚本（action_submit.py）以及脚本依赖和action配置文件（.github/workflows/main.yml），以下为使用方法：

直接fork到自己仓库，然后添加自己信息，就可使用。

首先，将自己的用户名和密码保存到仓库的 secrets 下，如图

首先点击仓库上方 Settings，然后点击 secrets

![](https://github.com/Swenchao/bjut_clock/blob/master/images/1.png)

然后新增一个新的 secrets

![](https://github.com/Swenchao/bjut_clock/blob/master/images/2.png)

最后以k-v形式输入你的账号和密码以及申请的server的key值（没有申请，这个可以不添加，不影响使用）

username ：学号
password ：密码
key ：申请的server的key

![](https://github.com/Swenchao/bjut_clock/blob/master/images/3.png)

然后点击仓库上面的action

![](https://github.com/Swenchao/bjut_clock/blob/master/images/5.png)

点击那个长条按钮，因为我这已经添加，所以没有那个界面了.就是一直走肯定的回答，往下走就可以了，最后是这样的

![](https://github.com/Swenchao/bjut_clock/blob/master/images/4.png)

然后可以随便修改一点地方提交一下也会自动触发，这样可以检验下自己的是否成功。如果成功了就会在每天九点准时打卡了，不过消息推送会推迟10几分钟左右~

