import random

import requests
from requests import adapters
import json
from .xid import encode_xid

adapters.DEFAULT_RETRIES = 5

header = {
    "accept-encoding": "gzip",
    "client": "app",
    "client-version": "2.20.39",
    "content-type": "application/json; charset=utf-8",
    "host": "api.jikipedia.com",
    "user-agent": "jikidia_app_google_emu64x_Android_13_33_TE1A.220922.012_d79c2787-e3b6-446d-8d52-edd80a72a414"
}


class Jikipedia:
    # 获取 用户基础信息
    def __init__(self, phone=None, password=None, cookie_user=None, cookie_xid=None, domain='api.jikipedia.com',
                 xid_api="http://127.0.0.1:3000"):
        self.session = requests.Session()
        self.phone = phone
        self.password = password
        self.domain = domain
        self.author_id = None
        self.xid_api = xid_api  # TODO(daizihan233): 呃呃呃 别问这是个啥，问就是还没开发好（详见第 41 行注释）
        if phone and password:
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
            # ! 算法在写了 别催了（除非你能帮我找到 XIDSecret | 这个密钥或许藏在 APK 里，当然鸡典使用的是 Flutter 框架，逆向起来很蓝的啦~）
            # self.xid = encode_xid(xid_api=xid_api)
            # ? 鸡典的 XID 算法中，并没有考虑时间和账号因素，所以理论上一个 XID 可以所有账号通用，并且没有时间期限
            self.xid = "vRUFu93dvOFKGK4PehwZjVO9x6CelYgy2KCkbbeL9lJKlTuV+sMZn43FR/rfIlpBCqW2k7BGzkJmHGOiJ63HY1S0w4TMGd58hFnAKU7OnmbTTAx8S8bJzokn3d9SLJvpNTHbwlKP+IrKhlffIMxTDg=="
        else:
            if cookie_user and cookie_xid:
                self.token = cookie_user['token']
                self.xid = encode_xid(cookie_xid, xid_api)
            else:
                raise ValueError("您搁这儿零元购呢？账号密码token全不给你让我怎么登录？？？")

    # 获取 搜索栏的推荐
    def get_search_recommend(self) -> dict:
        return self._requests_jikipedia_api(url=f'https://{self.domain}/wiki/request_search_placeholder',
                                            method="GET",
                                            return_type='dict')

    # 调用 恶魔鸡翻译器
    def emoji(self, text) -> str:
        data = {
            'content': str(text)
        }
        data = json.dumps(data)
        return \
            self._requests_jikipedia_api(url=f'https://{self.domain}/go/translate_plaintext', parameter=data,
                                         method="POST",
                                         return_type="dict")['translation']

    def _requests_jikipedia_api(self, url: str, parameter=None, method: str = "GET",
                                return_type: str = "dict",
                                has_token: bool = True, has_xid: bool = True, dump=True):
        if parameter is None:
            parameter = {}
        try:
            headers = header.copy()
            if has_xid:
                headers['XID'] = self.xid
                headers['Token'] = self.token
            if dump:
                t = self.session.request(method, url, url, data=json.dumps(parameter), headers=headers)
            else:
                t = self.session.request(method, url, url, data=parameter, headers=headers)

            if t.status_code == 401:
                self.token = self.get_token()
                # self.xid = encode_xid(xid_api=self.xid_api)
                return self._requests_jikipedia_api(url, parameter, method, return_type, has_token, has_xid, dump)
            elif t.status_code == 412:  # 这里有个Bug，但貌似只能用这个笨办法解决
                return self._requests_jikipedia_api(url, parameter, method, return_type, has_token, has_xid, not dump)
            elif t.status_code == 404:
                raise ConnectionError("呜呜呜…… 这个API不！存！在！")
            elif 500 > t.status_code >= 200:  # 正常返回 2xx 3xx 4xx
                if return_type.upper() == "DICT":
                    return json.loads(t.text)
                elif return_type.upper() == "OBJ":
                    return t
            else:
                raise ConnectionError(f"HTTPError: Status_code = {t.status_code}")
        except ValueError:
            raise ConnectionError(
                "由于 Python requests 的特色，请关闭你的梯子，不过产生此报错的原因有很多，如有其它问题请提交Issue")
        raise RuntimeError(f'未知的错误！以下信息仅供参考：\n'
                           f'url = {url}\n'
                           f'parameter = {parameter}\n'
                           f'method = {method}\n'
                           f'return_type = {return_type}\n'
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
            r = self._requests_jikipedia_api(url=f'https://{self.domain}/wiki/phone_password_login',
                                             parameter=data,
                                             method="POST",
                                             return_type="Obj",
                                             has_token=False,
                                             has_xid=False)
            self.author_id = r.json()['id']
            if r.status_code != 200:
                raise RuntimeError(
                    f'手机号码或密码错误，请依次检查网络连接、手机号/密码是否正确: {json.dumps(json.loads(r.text), indent=4)}')
            return json.loads(r.text)
        else:
            raise RuntimeError("因为使用了 cookie 登录所以无法重新登录以自动获取 token")

    # 获取 Token
    def get_token(self) -> dict:
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
        r = self._requests_jikipedia_api(url=f'https://{self.domain}/go/set_definition_like', parameter=data,
                                         method="POST",
                                         return_type="Obj")
        return r.status_code

    # 进行 签到
    def sign(self) -> bool:
        return \
            self._requests_jikipedia_api(url=f'https://{self.domain}/wiki/new_check_in', parameter={},
                                         method="POST",
                                         return_type="dict")['first']

    # 调用 活动-我们的维权API
    def gather_event_hope(self, count: int = 2000) -> int:
        payload = {
            "event": "weibo",
            "count": count
        }

        response = self._requests_jikipedia_api(url=f'https://{self.domain}/go/gather_event_hope', parameter=payload,
                                                method="POST",
                                                return_type="OBJ")
        if response.status_code != 400:
            return response.json()['count']
        else:
            return 0

    # 进行 补签
    def ssign(self, year: int, month: int, day: int) -> int:
        data = {
            'date': '{}-{}-{}'.format(year, month, day)
        }
        return self._requests_jikipedia_api(url=f'https://{self.domain}/wiki/new_check_in', method="POST",
                                            parameter=data,
                                            return_type="Obj").status_code

    # 热搜榜获取
    def get_hot(self):
        return self._requests_jikipedia_api(url=f"https://{self.domain}/go/get_hot_search",
                                            parameter={},
                                            method="POST",
                                            return_type="dict")

    # 获取 热门活动
    def browse_banners(self) -> dict:
        return self._requests_jikipedia_api(url=f"https://{self.domain}/go/browse_banners",
                                            parameter={"location": "activity"},
                                            method="POST",
                                            return_type="dict")

    # 获取 首页推荐
    def get_home(self):
        return self._requests_jikipedia_api(url=f"https://{self.domain}/go/browse_entities",
                                            parameter={},
                                            method="POST",
                                            return_type="dict")

    # 进行 评论
    def comment(self, definition: int, text: str, reply: int = 0) -> dict:
        data = {
            'content': text,
            'entity_category': 'definition',
            'entity_id': definition,
            'reply_to': reply
        }

        return self._requests_jikipedia_api(url=f'https://{self.domain}/wiki/request_search_placeholder',
                                            method="POST", parameter=data,
                                            return_type="dict")

    # 获取 当前用户 / 指定用户 的所有词条
    def request_created_definition(self, uid: int = None, page: int = 1):
        if uid is None:
            uid = self.author_id
        data = {
            "author_id": uid,
            "page": page,
            "mode": "full",
            "filter": "normal",
            "sort_by": "hot",
            "category": "normal",
            "include_anonymous": True
        }
        return self._requests_jikipedia_api(url=f'https://{self.domain}/go/request_created_definition',
                                            method="POST", parameter=data,
                                            return_type="dict")
