# -*- coding: utf-8 -*-
import requests
import json
import sys
import logging  
import logging.handlers
import socket
import urllib
import os

localIP = socket.gethostbyname(socket.gethostname())

def main():
    headers = {'content-type': 'application/json'}
    url = 'http://'+ sys.argv[2] + ":4000/jsonrpc"
    payload = {
        'method': 'get',
        'params': [{}],
        'jsonrpc': '2.0',
        'id': 0
    }

    cmdType = sys.argv[1]

    if cmdType == 'syuc':
        payload["params"][0]['cmdType'] = cmdType
        payload["params"][0]['url'] = 'http://'+ sys.argv[2] + ":4000/jsonrpc"
        payload["params"][0]['cmd'] = sys.argv[3]
        payload["params"][0]['address'] = localIP
    elif cmdType == 'download':
        payload["params"][0]['cmdType'] = cmdType
        payload["params"][0]['url'] = 'http://'+ sys.argv[2] + ":4000/jsonrpc"
        payload["params"][0]['serverPath'] = sys.argv[3]
        payload["params"][0]['localPath'] = sys.argv[4]
        payload["params"][0]['address'] = localIP
    # Example echo method

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    
    dataStr = json.dumps(response)

    # 写入文件 
    if cmdType == 'download' and response['result']['file'] != 'false':
        output = open( payload["params"][0]['localPath'] , 'w')
        file = response["result"]["file"]
        output.write(file)

    print(dataStr)

if __name__ == '__main__':
    main()
