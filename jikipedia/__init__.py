import random
import requests
import json
import base64


# 生成 明文XID（纯Python实现）
def generate_plaintext_xid() -> str:
    xid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    xid = [str(x) for x in xid[::-1]]
    for s in range(len(xid)):
        if xid[s] == 'x':
            r = int(random.random() * 16)
            xid[s] = str(hex(r))[2:]
        elif xid[s] == 'y':
            r = int(random.random() * 16)
            xid[s] = str(hex(3 & r | 8))[2:]
    return ''.join(xid)[::-1]


# 加密 明文XID
def encode_xid(xid=None) -> str:
    if xid is None:
        xid = generate_plaintext_xid()
    xid = base64.encodebytes(("jikipedia_xid_" + xid).encode('utf-8'))
    return str(xid.decode('utf-8')).strip('\n')


# 获取 搜索栏的推荐
def get_search_recommend() -> dict:
    s = requests.get('https://api.jikipedia.com/wiki/request_search_placeholder').text
    s = json.loads(s)
    return s


# 调用 恶魔鸡翻译器
def emoji(text) -> str:
    data = {
        'content': str(text)
    }
    data = json.dumps(data)
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    r_p = requests.post(url='https://api.jikipedia.com/go/translate_plaintext', data=data, headers=head)
    return json.loads(r_p.text)['translation']


class Jikipedia:
    # 获取 用户基础信息
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password
        if type(phone) != str:
            if type(phone) == int:
                self.phone = str(phone)
            else:
                raise TypeError('phone 参数类型错误，应为 str 或 int，而不是 {}'.format(type(phone)))
        if type(password) != str:
            raise TypeError('password 参数类型错误，应为 str，而不是 {}'.format(type(password)))
        if len(phone) != 11:
            raise ValueError('手机号码长度不正确')

    # 模拟登录获取更多信息
    def login(self) -> dict:
        data = {
            'password': self.password,
            'phone': self.phone
        }
        data = json.dumps(data)
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Client': 'web',
            'Client-Version': '2.6.12k',
            'Connection': 'keep-alive',
            'Content-Length': '48',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'api.jikipedia.com',
            'Origin': 'https://jikipedia.com',
            'Pragma': 'no-cache',
            'Referer': 'https://jikipedia.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'XID': encode_xid()
        }
        r = requests.post('https://api.jikipedia.com/wiki/phone_password_login',
                          data=data,
                          headers=header)
        if r.status_code != 200:
            raise RuntimeError('手机号码或密码错误，请依次检查网络连接、手机号/密码是否正确')
        return json.loads(r.text)

    # 获取 Token
    def get_token(self) -> str:
        try:
            return self.login()['token']
        except KeyError or ValueError:
            raise RuntimeError('手机号码或密码错误，请依次检查网络连接、手机号/密码是否正确')

    # 进行 对词条 （取消）点赞
    def like(self, id_: int, status: bool = True) -> int:
        data = {
            'id': id_,
            'status': status
        }
        data = json.dumps(data)
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Client': 'web',
            'Client-Version': '2.6.12k',
            'Connection': 'keep-alive',
            'Content-Length': '30',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'api.jikipedia.com',
            'Origin': 'https://jikipedia.com',
            'Pragma': 'no-cache',
            'Referer': 'https://jikipedia.com/',
            'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Token': self.get_token(),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56/H6avzxdHX',
            'XID': encode_xid()
        }
        r = requests.post('https://api.jikipedia.com/go/set_definition_like', data=data, headers=header)
        return r.status_code

    # 进行 签到
    def sign(self) -> bool:
        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'Client-Version': '2.6.11b',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
            'Client': 'web',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://jikipedia.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://jikipedia.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,nl;q=0.5',
        }
        headers.update({'XID': encode_xid(), 'Token': self.get_token()})

        r = requests.post('https://api.jikipedia.com/wiki/new_check_in', headers=headers, data='{}')

        return json.loads(r.text)['first']

    # 调用 活动-我们的维权API
    def gather_event_hope(self, count: int = 2000) -> int:
        payload = {
            "event": "weibo",
            "count": count
        }
        headers = {
            'Connection': 'close',
            'XID': encode_xid(),
            'Content-Type': 'application/json;charset=utf-8',
            'Token': self.get_token()
        }
        tmp_json = requests.post('https://api.jikipedia.com/go/gather_event_hope', headers=headers,
                                 data=json.dumps(payload)).text
        tmp_json = json.loads(tmp_json)
        try:
            return tmp_json['count']
        except ValueError:
            return 0

    # 进行 补签
    def ssign(self, year: int, month: int, day: int) -> int:
        headers = {
            'Token': self.get_token(),
            'XID': encode_xid(),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = {
            'date': '{}-{}-{}'.format(year, month, day)
        }
        r = requests.post('https://api.jikipedia.com/wiki/new_check_in', headers=headers, data=json.dumps(data))
        return r.status_code

    # 进行 评论
    def comment(self, definition: int, text: str, reply: int = 0) -> dict:
        headers = {
            'Token': self.get_token(),
            'XID': encode_xid(),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = {
            'content': text,
            'entity_category': 'definition',
            'entity_id': definition,
            'reply_to': reply
        }
        r = requests.post('https://api.jikipedia.com/go/create_comment', data=data, headers=headers)
        return json.loads(r.text)

    # 获取 新增词条数量
    def jk(self) -> int:
        headers = {
            'Token': self.get_token(),
            'XID': encode_xid(),
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = {}
        r = requests.post('https://api.jikipedia.com/wiki/cocore_2022_jk_definition_count', data=data, headers=headers)
        return json.loads(r.text)['count']
