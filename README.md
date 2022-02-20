## **_jikipedia-api_**
注意：该项目还在开发完善中，有Bug欢迎反馈
### 相关页面导航栏
[小鸡词典 Jikipedia](https://jikipedia.com/) <br>
[作者主页 @Bug鸡](https://jikipedia.com/definitions/user/281250396) <br>
[Github项目]()
### 做了些什么？
#### 互动类
- [ ] 签到
- [ ] 收藏
- [ ] 点赞
- [ ] 评论
- [ ] 关注
#### 数据类
- [x] 生成XID
- [ ] 获取XID
- [ ] 加密XID
- [ ] 解密XID
- [x] Token获取
- [ ] 被阅读、点赞的数据
- [ ] 个人信息
- [ ] 关注（者）
- [ ] 粉丝（者）
- [ ] 词条内容
- [ ] 词条编写者
#### 创作类
- [ ] 词条
- [ ] 杂谈
#### 活动类
- [x] 恶魔鸡翻译器
### 食用教程
#### 安装
```
pip install jikipedia-api
```
#### import
```
from jikipedia-api import Jikipedia
```
如果出现ImportError，请检查是否安装了requests、json、execjs。
#### 初始化
```
jikipedia = Jikipedia(phone=12345678901, password='123456')
```
phone 是 11 位手机号，password 是 密码。
#### 生成明文XID
```
xid = jikipedia.generate_plaintext_xid()
```
xid 为 str 类型，可以直接使用。
#### Token获取
```
token = jikipedia.get_token()
```
token 为 str 类型，可以直接使用。
#### 恶魔鸡翻译器
```
jikipedia.emoji('你好')
```
参数必须为 str 类型，返回值为 str 类型，即翻译之后的内容。
