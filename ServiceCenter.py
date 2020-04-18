import json
import time
import Tecent_Authentication as txauth
import random
import requests
import UserManger

class ServiceCenter(object):
    def __init__(self, conf_path):
        self.read_conf(conf_path)

    def read_conf(self, path):
        file = open(path)
        self.conf = json.load(file)
        file.close()

    def save_conf(self, path):
        file = open(path, 'w')
        json.dump(self.conf, file, indent=4)
        file.close()

    def tecent_translate(self, text):
        url = self.conf['tencent_ai_translation']['url']
        params = {
            'app_id': self.conf['tencent_ai_config']['app_id'],
            'time_stamp': int(time.time()),
            'nonce_str': txauth.GetRandomStr(length=15),
            'text': text,
            'source': 'zh',
            'target': 'en'
        }
        params['sign'] = txauth.GetSign(params, self.conf['tencent_ai_config']['app_key'])

        res = requests.post(url, params).json()
        if (res['ret'] == 0):
            return res['data']['target_text']
        else:
            return res['msg']
        
    def tecent_talking(self, question, session):
        url = self.conf['tencent_ai_talking']['url']
        params = {
            'app_id': self.conf['tencent_ai_config']['app_id'],
            'time_stamp': int(time.time()),
            'nonce_str': txauth.GetRandomStr(length=15),
            'session': session,
            'question': question
        }
        params['sign'] = txauth.GetSign(params, self.conf['tencent_ai_config']['app_key'])

        res = requests.post(url, params).json()
        if (res['ret'] == 0):
            return res['data']['answer']
        else:
            return res['msg']
            


    
