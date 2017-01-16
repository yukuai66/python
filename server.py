# -*- coding: utf-8 -*-
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import os
import json
import sys
import time

reload(sys)
sys.setdefaultencoding('UTF-8')
path = os.getcwd()

@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]

@Request.application
def application(request):

    # Dispatcher is dictionary {<method_name>: callable}
    # dispatcher["echo"] = lambda s: s
    # dispatcher["add"] = lambda a, b: a + b
    jo = json.loads(request.data)

    cmdType = jo["params"][0]["cmdType"]
    errorMesage = ''
    #写入日志

    if cmdType == "syuc":
        cmd = jo["params"][0]["cmd"]
        state = os.system(cmd)
        var = os.popen(cmd).read().decode('utf-8', 'ignore')
        if state == 1:
            var = 'error'
            errorMesage = '   错误 : 指令错误'
        if os.path.isdir(path+'/log.txt'):
            file = open('log.txt','w')
            file.writelines("Time :" + time.strftime("%Y/%m/%d %I:%M:%S") + "   IP :" + jo["params"][0]["address"] + "   Command :" + cmd + errorMesage +"\n")
        else:
            file = open('log.txt','a')
            file.writelines("Time :" + time.strftime("%Y/%m/%d %I:%M:%S") + "   IP :" + jo["params"][0]["address"] + "   Command :" + cmd + errorMesage +"\n")

        dispatcher['get']  = lambda d : {"success": "true","resule": 1,'shell':var}

    #读取文件
    elif cmdType == 'download':
        try:
            file_object = open(jo["params"][0]["serverPath"])
        except IOError:
            errorMesage = '   错误 : 文件错误'
            dispatcher['get']  = lambda d : {"success": "true","resule": 1,"file":'false'}
        else:
            try:
                all_the_text = file_object.read( )
            finally:
                dispatcher['get']  = lambda d : {"success": "true","resule": 1,"file":all_the_text}
                file_object.close( )

        if os.path.isdir(path+'/log.txt'):
            file = open('log.txt','w')
            file.writelines("Time :" + time.strftime("%Y/%m/%d %I:%M:%S") + "   IP :" + jo["params"][0]["address"] + "   Command :" + jo["params"][0]["cmdType"] + errorMesage +"\n")
        else:
            file = open('log.txt','a')
            file.writelines("Time :" + time.strftime("%Y/%m/%d %I:%M:%S") + "   IP :" + jo["params"][0]["address"] + "   Command :" + jo["params"][0]["cmdType"] + errorMesage +"\n")

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')

if __name__ == '__main__':
    run_simple( '0.0.0.0', 4000, application)
