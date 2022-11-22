answer = ""
sqlIngection = {}
information = {}
v1 = None
s1 = None
check = []
result = {}
table_name = ''
column_name = ''
union = [0,0]
def _init():
    global answer
    global sqlIngection
    global information
    global degree
    answer = "start\n"
    sqlIngection = {}
    information = {
        'url1': "",
        'id1': None,
        'method1': None,
        'column1': None,
        'value1': 0,
        'v1': None,
        'degree': "0",
        'bugName': ""
    }


def set_answer(value):
    global answer
    answer = value


def set_sqlIngection(key, value):
    global sqlIngection
    sqlIngection[key] = value

def set_result(key, value):
    global result
    if key in result.keys():
        result[key] += value
    else:
        result[key] = value


def set_infor(key, value):
    global information
    information[key] = value


def get_answer(defValue=None):
    global answer
    try:
        return answer
    except KeyError:
        return defValue


def get_sqlIngection(defValue=None):
    global sqlIngection
    try:
        return sqlIngection
    except KeyError:
        return defValue


def get_infor(key, defValue=None):
    global information
    try:
        return information[key]
    except KeyError:
        return defValue
