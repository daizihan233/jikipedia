import requests
import json
import execjs


class Jikipedia:
    # 获取 用户基础信息
    def __init__(self, phone: int, password: str):
        self.phone = phone
        self.password = password

    def login(self):
        data = {
            'phone': self.phone,
            'password': self.password
        }
        r = requests.post('https://api.jikipedia.com/wiki/phone_password_login', data=json.dumps(data))
        return json.loads(r.text)

    def get_token(self):
        return Jikipedia.login(self)['token']

    # 生成 明文XID
    def generate_plaintext_xid(self):
        xid = execjs.compile('''function get_xid(){    const xid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, 
        (function (name) {
          let randomInt = 16 * Math.random() | 0;
          return ("x" === name ? randomInt : 3 & randomInt | 8).toString(16)
        }));return xid;}
        ''')
        return xid.call('get_xid')

    # 调用 恶魔鸡翻译器
    def emoji(self, text):
        data = {
            'content': str(text)
        }
        data = json.dumps(data)
        head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
        r_p = requests.post(url='https://api.jikipedia.com/go/translate_plaintext', data=data, headers=head)
        return json.loads(r_p.text)['translation']

