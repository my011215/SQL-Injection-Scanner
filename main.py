from flask import Flask, render_template, request
from scan import Vulnerability
import glo
from sql import sqli
import json

# coding:utf-8

app = Flask(__name__)


@app.route('/')
def zhuye():
    return render_template('主页.html')


@app.route('/BugSearch2')
def BugSearch2():
    glo.v1.run()
    print(1)
    return render_template('漏洞扫描2.html')


@app.route('/BugSearch0')
def poiling():
    return glo.get_answer()


@app.route('/degree')
def degree():
    degree = glo.get_infor('degree')
    return degree


@app.route('/bugName')
def bugName():
    bugName = glo.get_infor('bugName')
    return bugName


@app.route('/BugSearch1')
def BugSearch1():
    return render_template('漏洞扫描1.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'))


@app.route('/judge')
def judge():
    if glo.v1 is not None:
        return render_template('sql注入复选框.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), id=glo.get_infor('id1'))
    else:
        return render_template('sql注入首页.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'),
                               id=glo.get_infor('id1'))



@app.route('/SQL1')
def SQL1():
    return render_template('sql注入复选框.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), id=glo.get_infor('id1'))

@app.route('/SQL2')
def SQL2():
    return render_template('sql手动配置.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'))

@app.route('/SQL3', methods=['POST'])
def SQL3():
    glo.answer = ''
    glo.check = request.form.getlist('check')
    glo.s1 = sqli(glo.get_infor("id1"), glo.get_infor("url1"), glo.get_infor("value1"), glo.get_infor("column1"), glo.get_infor("method1"))
    return render_template('sql注入结果回显.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), id=glo.get_infor('id1'))

@app.route('/SQL3')
def poiling_SQL3():
    glo.result = {}
    glo.table_name = ''
    glo.column_name = ''
    print(glo.v1)
    if glo.union[0] == 0 or glo.union[1] == 0:
        union = glo.v1.union
        glo.union = glo.v1.union
    else:
        union = glo.union
    print(glo.information)
    glo.s1.run(glo.check, union)
    print(union)
    return render_template('sql注入结果回显.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), id=glo.get_infor('id1'))

@app.route('/SQL4', methods=['POST'])
def SQL4():
    glo.table_name = request.values.get('tableName')
    return render_template('sql结果回显1.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), table_name=glo.table_name)

@app.route('/SQL4')
def SQL04():
    glo.s1.run_columnName(glo.check, glo.table_name, glo.union)
    return render_template('sql结果回显1.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'))

@app.route('/SQL5', methods=['POST'])
def SQL5():
    glo.column_name = request.values.get('columnName')
    return render_template('sql结果回显2.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), column_name=glo.column_name)

@app.route('/SQL5')
def SQL05():
    glo.s1.run_columnData(glo.check, glo.table_name, glo.column_name, glo.union)
    return render_template('sql结果回显2.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'))

@app.route('/SQL6', methods=['POST'])
def SQL6():
    return render_template('sql注入抽屉.html', sqlIngection=glo.get_sqlIngection(), url=glo.get_infor('url1'), re=glo.result)


# @app.route('/SQL')
# def SQL():
#     union = [3, 2]
#     print(glo.information)
#     glo.s1.run(glo.check, union)
#     print(1)
#     return render_template('漏洞扫描2.html')

@app.route('/SQL0')
def SQL0():
    return glo.get_answer()


@app.route('/handle', methods=['POST'])
def handle():
    url1 = request.values.get('url')
    glo.set_infor('url1', url1)
    print(url1)
    id1 = request.values.get('id')
    glo.set_infor('id1', id1)
    print(id1)
    method1 = request.values.get('method')
    glo.set_infor('method1', method1)
    print(method1)
    column1 = request.values.get('column')
    if(method1 =='post'):
        column1 = json.loads(column1)
    glo.set_infor('column1', column1)
    print(column1)
    value1 = request.values.get('value')
    glo.set_infor('value1',value1)
    print(value1)
    close = request.values.get('close')
    print(close)
    exegesis = request.values.get('exegesis')
    print(exegesis)
    position = request.values.get('position')
    print(position)
    column_num = request.values.get('columnNum')
    print(column_num)
    glo.union[0] = int(column_num)
    glo.union[1] = int(position)
    if url1 == "":
        print('url1='+url1)
        return render_template('漏洞扫描2.html')
    else:
        glo.v1 = Vulnerability(url1, id1, column1, method1, value1)
        glo.s1 = sqli(id1, url1, value1, column1, method1, close, exegesis, position, column_num)
    return render_template('sql注入复选框.html', v1=glo.v1, url=url1, id=id1, column1=column1, method1=method1, value1=value1)


@app.route('/BugSearch2', methods=['POST'])
def search():
    url1 = request.values.get('url1')
    glo.set_infor('url1', url1)
    print(url1)
    id1 = request.values.get('id1')
    glo.set_infor('id1', id1)
    print(id1)
    method1 = request.values.get('method1')
    glo.set_infor('method1', method1)
    print(method1)
    column1 = request.values.get('column1')
    if(method1 =='post'):
        column1 = json.loads(column1)
    glo.set_infor('column1', column1)
    print(column1)
    value1 = request.values.get('value1')
    glo.set_infor('value1',value1)
    print(value1)
    if url1 == "":
        print('url1='+url1)
        return render_template('漏洞扫描2.html')
    else:
        glo.sqlIngection = {}
        glo.v1 = Vulnerability(url1, id1, column1, method1, value1)
    return render_template('漏洞扫描2.html', v1=glo.v1, url1=url1, id1=id1, column1=column1, method1=method1, value1=value1)


if __name__ == '__main__':
    glo._init()
    app.run()
