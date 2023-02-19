import json
import uuid

import requests


# 加密 明文XID
def aes_crypto(text, xid_api="https://jiki.online"):
    # ? 本人自建的 API
    # * Python 中，AES 的密钥必须是长 16 byte / 32 byte
    # * 后端使用 nodejs 并使用 CryptoJS 进行加密
    # * 有一个很有意思的点就是 CryptoJS 不限制密钥长度
    # ! 如果你需要自己部署，请见 项目文件 中的 [get_xid.js]
    data = requests.get(f"{xid_api}/jiki/encrypt/xid", params={
        "xid": text
    }).text
    print(data)
    return json.loads(data)['encode_xid']


def encode_xid(xid=None, xid_api="https://jiki.online") -> str:
    crypt = aes_crypto(xid, xid_api)
    return crypt
