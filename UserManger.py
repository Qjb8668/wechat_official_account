import json
import requests

class UserManager(object):
    def __init__(self, userlist_path):
        self.userlist_path = userlist_path
        self.read_userlist()

    def read_userlist(self):
        file = open(self.userlist_path)
        self.users = json.load(file)
        file.close()

    def save_userlist(self):
        file = open(self.userlist_path, 'w')
        json.dump(self.users, file, indent=4)
        file.close()

    def getUserByOpenid(self, openid):
        for user in self.users:
            if user['openid'] == openid:
                return user
        
        return None

    def new_user(self, openid, mode=0):
        user = {
            'openid': openid,
            'mode': mode
        }
        return user

    def addNewUser(self, openid, mode=0):
        if not self.getUserByOpenid(openid):
            user = self.new_user(openid, mode)
            self.users.append(user)
            self.save_userlist()

    def update_users(self, url, access_token):
        next_openid = ''
        new_users = []
        while True:
            params = {
                'access_token': access_token,
                'next_openid': next_openid
            }
            res = requests.get(url, params).json()
            if ('errcode' in res):
                print('Get assess_token error: ' + str(res['errcode']) + ' ' + res['errmsg'])
                break

            for openid in res['data']['openid']:
                user = self.getUserByOpenid(openid)
                if user:
                    new_users.append(user)
                else:
                    new_users.append(self.new_user(openid, mode=0))
            
            next_openid = res['next_openid']
            if (res['count'] < 10000):
                break

        self.users = new_users
        self.save_userlist()



    