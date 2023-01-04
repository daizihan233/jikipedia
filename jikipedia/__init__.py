import random
import requests
from requests import adapters
import json
import base64

adapters.DEFAULT_RETRIES = 5

user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Client': 'web',
    'Connection': 'close',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://jikipedia.com',
    'Pragma': 'no-cache',
    'Referer': 'https://jikipedia.com/',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': random.choice(user_agent_list)
}


class Jikipedia:
    # 获取 用户基础信息
    def __init__(self, phone=None, password=None, cookie=None, domain='api.jikipedia.com'):
        if phone and password:
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
            self.token = self.get_token()
            self.xid = self.encode_xid()
        else:
            if not cookie:
                self.token = cookie['token']
                self.xid = cookie['XID']
            else:
                raise ValueError("您搁这儿零元购呢？账号密码token全不给你让我怎么登录？？？")
        self.domain = domain

    # 生成 明文XID（纯Python实现）
    @staticmethod
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
    def encode_xid(self, xid=None) -> str:
        if xid is None:
            xid = self.generate_plaintext_xid()
        xid = base64.encodebytes(("jikipedia_xid_" + xid).encode('utf-8'))
        return str(xid.decode('utf-8')).strip('\n')

    # 获取 搜索栏的推荐
    def get_search_recommend(self) -> dict:
        return self._requests_jikipedia_api(u=f'https://{self.domain}/wiki/request_search_placeholder', m=requests.get,
                                            r='dict')

    # 调用 恶魔鸡翻译器
    def emoji(self, text) -> str:
        data = {
            'content': str(text)
        }
        data = json.dumps(data)
        return \
            self._requests_jikipedia_api(u=f'https://{self.domain}/go/translate_plaintext', p=data, m=requests.post,
                                         r="dict")['translation']

    def _requests_jikipedia_api(self, u: str, p=None, m: requests.post or requests.get = requests.get, r: str = "dict",
                                has_token: bool = True, has_xid: bool = True, dump=True):
        if p is None:
            p = {}
        try:
            if dump:
                t = m(u, data=json.dumps(p), headers=header)
            else:
                t = m(u, data=p, headers=header)
            if t.status_code == 401:
                self.token = self.get_token()
                self.xid = self.encode_xid()
                return self._requests_jikipedia_api(u, p, m, r, has_token, has_xid, dump)
            elif t.status_code == 412:  # 这里有个Bug，但貌似只能用这个笨办法解决
                return self._requests_jikipedia_api(u, p, m, r, has_token, has_xid, not dump)
            elif 300 > t.status_code >= 200:
                if r.upper() == "DICT":
                    return json.loads(t.text)
                elif r.upper() == "OBJ":
                    return t
            else:
                raise ConnectionError(f"HTTPError: Status_code = {t.status_code}")
        except ValueError:
            raise ConnectionError(
                "由于 Python requests 的特色，请关闭你的梯子，不过产生此报错的原因有很多，如有其它问题请提交Issue")
        raise RuntimeError(f'未知的错误！以下信息仅供参考：\n'
                           f'u = {u}\n'
                           f'p = {p}\n'
                           f'm = {m}\n'
                           f'r = {r}\n'
                           f'has_token = {has_token}\n'
                           f'has_xid = {has_xid}\n'
                           f'status_code = {t.status_code}')

    # 模拟登录获取更多信息
    def login(self) -> dict:
        if self.phone and self.password:
            data = {
                'password': self.password,
                'phone': self.phone
            }
            data = json.dumps(data)
            r = self._requests_jikipedia_api(u=f'https://{self.domain}/wiki/phone_password_login',
                                             p=data,
                                             m=requests.post,
                                             r="Obj",
                                             has_token=False,
                                             has_xid=False)
            if r.status_code != 200:
                raise RuntimeError(
                    f'手机号码或密码错误，请依次检查网络连接、手机号/密码是否正确: {json.dumps(json.loads(r.text), indent=4)}')
            return json.loads(r.text)
        else:
            raise RuntimeError("因为使用了 cookie 登录所以无法重新登录以自动获取 token")

    # 获取 Token
    def get_token(self) -> str:
        try:
            return self.login()['token']
        except KeyError:
            raise RuntimeError(f'手机号码或密码错误，请依次检查网络连接、手机号/密码是否正确')
        except ValueError:
            raise RuntimeError(f'手机号码或密码错误，请依次检查网络连接、手机号/密码是否正确')

    # 进行 对词条 （取消）点赞
    def like(self, id_: int, status: bool = True) -> int:
        data = {
            'id': id_,
            'status': status
        }
        data = json.dumps(data)
        r = self._requests_jikipedia_api(u=f'https://{self.domain}/go/set_definition_like', p=data, m=requests.post,
                                         r="Obj")
        return r.status_code

    # 进行 签到
    def sign(self) -> bool:
        return self._requests_jikipedia_api(u=f'https://{self.domain}/wiki/new_check_in', p={}, m=requests.post,
                                            r="dict")['first']

    # 调用 活动-我们的维权API
    def gather_event_hope(self, count: int = 2000) -> int:
        payload = {
            "event": "weibo",
            "count": count
        }

        try:
            return \
                self._requests_jikipedia_api(u=f'https://{self.domain}/go/gather_event_hope', p=payload,
                                             m=requests.post,
                                             r="Obj")['count']
        except ValueError:
            return 0

    # 进行 补签
    def ssign(self, year: int, month: int, day: int) -> int:
        data = {
            'date': '{}-{}-{}'.format(year, month, day)
        }
        return self._requests_jikipedia_api(u=f'https://{self.domain}/wiki/new_check_in', m=requests.post,
                                            p=data,
                                            r="Obj").status_code

    # 热搜榜获取
    def get_hot(self):
        return self._requests_jikipedia_api(u=f"https://{self.domain}/go/get_hot_search",
                                            p={},
                                            m=requests.post,
                                            r="dict")

    # 获取 热门活动
    def browse_banners(self) -> dict:
        return self._requests_jikipedia_api(u=f"https://{self.domain}/go/browse_banners",
                                            p={"location": "activity"},
                                            m=requests.post,
                                            r="dict")

    # 获取 首页推荐
    def get_home(self):
        return self._requests_jikipedia_api(u=f"https://{self.domain}/go/browse_entities",
                                            p={},
                                            m=requests.post,
                                            r="dict")

    # 进行 评论
    def comment(self, definition: int, text: str, reply: int = 0) -> dict:
        data = {
            'content': text,
            'entity_category': 'definition',
            'entity_id': definition,
            'reply_to': reply
        }

        return self._requests_jikipedia_api(u=f'https://{self.domain}/wiki/request_search_placeholder',
                                            m=requests.post, p=data,
                                            r="dict")
