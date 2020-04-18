import json
import hashlib
import requests
import time
import UserManger

class WechatCenter(object):
    def __init__(self, conf_path, userlist_path):
        self.conf_path = conf_path
        self.read_conf()
        
        self.update_token()

        self.userManger = UserManger.UserManager(userlist_path)

    def update_token(self):
        if (time.time() - self.conf['update_time'] >= 5000):
            url = self.conf['token_url']
            params = {
                "grant_type": "client_credential",
                "appid": self.conf['AppID'],
                "secret": self.conf['AppSecret']
            }
            
            res = requests.get(url, params).json()
            if ('errcode' in res):
                print('Get assess_token error: ' + str(res['errcode']) + ' ' + res['errmsg'])
            else:
                print(res['access_token'])
                self.conf['access_token'] = res['access_token']
                self.conf['update_time'] = time.time()
                self.save_conf()

        return

    def read_conf(self):
        file = open(self.conf_path)
        self.conf = json.load(file)
        file.close()

    def save_conf(self):
        file = open(self.conf_path, 'w')
        json.dump(self.conf, file, indent=4)
        file.close()

    def isWechatChecking(self, args):
        signature = args.get('signature')
        timestamp = args.get('timestamp')
        nonce = args.get('nonce')
        echostr = args.get('echostr')
        params = [self.conf['token'], timestamp, nonce]
        params.sort(reverse=False)
        string = str(params[0]) + str(params[1]) + str(params[2])
        mysign = hashlib.sha1(string.encode()).hexdigest()

        if (mysign == signature):
            return echostr
        else:
            return False
