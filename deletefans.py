#!/usr/bin/python
# coding=UTF-8
# noinspection PySingleQuotedDocstring
import requests
import time
import json
import re

cookie = input("Please input your account cookie:")
DedeUserID = re.findall("DedeUserID=[0-9]*",cookie,re.S)[0]
uid = re.findall("[0-9]*",DedeUserID,re.S)[0]
cookies = {}
for line in cookie.split(";"):
    if line.find("=") != -1:
        name, value = line.strip().split("=")
        cookies[name] = value
page = 1
ps = "50"
userid = []
infourl = "https://api.bilibili.com/x/relation/stat?vmid=" + uid
deletefansurl = "https://api.bilibili.com/x/relation/modify"
infodata = requests.get(url=infourl, cookies=cookies)
infolist = json.loads(infodata.text)
fannum = infolist['data']['follower']
if fannum > 1000:
    neednum = 20
    fansecond = neednum*15
    print("因系统限制，只能获取前20页粉丝内容，预计执行获取任务需要：" + str(fansecond) + "秒")
    while True:
        if page <= neednum:
            num = 0
            getfansurl = "https://api.bilibili.com/x/relation/followers?vmid=" + str(uid) + "&pn=" + str(page) + "&ps=" + str(ps)
            listdata = requests.get(url=getfansurl, cookies=cookies)
            pagelist = json.loads(listdata.text)
            while True:
                user = pagelist['data']['list'][num]['mid']
                userid.append(user)
                if num == 49:
                    break
                else:
                    num += 1
            page += 1
            time.sleep(15)
        else:
            break
else:
    neednum = int(fannum / 50)
    residuenum = fannum - neednum * 50
    fansecond = (neednum + 1) * 15
    print("预计执行获取任务需要" + str(fansecond) + "秒")
    while True:
        if page <= neednum:
            num = 0
            getfansurl = "https://api.bilibili.com/x/relation/followers?vmid=" + str(uid) + "&pn=" + str(page) + "&ps=" + str(ps)
            listdata = requests.get(url=getfansurl, cookies=cookies)
            pagelist = json.loads(listdata.text)
            while True:
                user = pagelist['data']['list'][num]['mid']
                userid.append(user)
                if num == 49:
                    break
                else:
                    num += 1
            page += 1
            time.sleep(15)
        else:
            num = 0
            ps = residuenum
            totalnum = residuenum - 1
            getfansurl = "https://api.bilibili.com/x/relation/followers?vmid=" + str(uid) + "&pn=" + str(page) + "&ps=" + str(ps)
            listdata = requests.get(url=getfansurl, cookies=cookies)
            pagelist = json.loads(listdata.text)
            while True:
                user = pagelist['data']['list'][num]['mid']
                userid.append(user)
                if num == totalnum:
                    break
                else:
                    num += 1
            break
nowtime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
f = open("fansuid-" + nowtime + ".txt", "a", encoding="utf-8")
print(userid, file=f)
f.flush()
if fannum > 1000:
    fannum = 1000
    deltime = fannum*5
else:
    deltime = fannum*5
print("粉丝获取完成，准备删除，预计执行删除任务需要" + str(deltime) + "秒")
headers = {
    "cookie": cookie,
    "referer": "https://space.bilibili.com/"+str(uid)+"/fans/fans",
    "origin": "https://space.bilibili.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
delnum = 0
arraynum = fannum - 1
bili_jct = re.findall("bili_jct=[0-9a-f]{32}",cookie,re.S)[0]
csrf = re.findall("[0-9a-f]{32}",bili_jct,re.S)[0]
while True:
    usermid = userid[delnum]
    data = {
        "fid": usermid,
        "act": "7",
        "re_src": "11",
        "csrf": csrf
    }
    requests.post(url=deletefansurl,data=data,headers=headers)
    time.sleep(5)
    if delnum == arraynum:
        break
    else:
        delnum += 1
print("执行完成，请手动检查执行结果")
