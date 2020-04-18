from flask import Flask, request
from handle import messageHandle
import WechatCenter
import ServiceCenter

wechat = WechatCenter.WechatCenter('./wechatConf.json', './userlist.json')
service = ServiceCenter.ServiceCenter('./serviceConf.json')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handleGetMenthod():
    res = wechat.isWechatChecking(request.args) # wechat check
    if (res != False):
        return res

@app.route('/', methods=['POST'])
def handlePostMethod():
    print('get it!')
    response = messageHandle(request.data, service, wechat)

    return response
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)