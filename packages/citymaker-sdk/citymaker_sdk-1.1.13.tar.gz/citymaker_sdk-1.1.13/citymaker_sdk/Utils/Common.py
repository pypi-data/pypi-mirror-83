#!/usr/bin/env Python
# coding=utf-8
#作者： tony
import json




# /**
#  * 对象属性转化小写(深度)
#  * @param {Object} data
#  */
def objtoLowerCase(data):
    if data is not None and type(data) is list:
        for item in data:
            item = objtoLowerCase(item)
    elif data is not None and type(data) is dict:
        for key in list(data.keys()):
            newKey = key[0].lower() + key[1:]
            if newKey == "picStream":
                data[newKey] = data[key]
                # data[newKey]=data.pop(key)
            else:
                data[newKey] = objtoLowerCase(data[key])
            if (newKey != key):
                del data[key]
    return data

def is_json(myjson):
    if myjson is None:
        return False
    if isinstance(myjson, str):
        try:
            json.loads(myjson)
        except ValueError:
            return False
        return True
    return False
def check_exsit(process_name):
    import win32com.client
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        return True
    else:
        return False
