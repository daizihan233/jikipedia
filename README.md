## **_jikipedia_**
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
- [x] 搜索栏的推荐
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
from jikipedia import Jikipedia
```
如果出现ImportError，请检查是否安装了requests、json、re。
#### 初始化
```
jiki = Jikipedia(phone=12345678901, password='123456')
```
phone 是 11 位手机号，password 是 密码。
#### 生成明文XID
```
xid = jiki.generate_plaintext_xid()
```
xid 为 str 类型，可以直接使用。
#### Token获取
```
token = jiki.get_token()
```
token 为 str 类型，可以直接使用。
#### 恶魔鸡翻译器
```
jiki.emoji('你好')
```
参数必须为 str 类型，返回值为 str 类型，即翻译之后的内容。
#### 搜索栏的推荐
```
jiki.get_search_recommend()
```
返回值为 dict 类型，即搜索栏的推荐。<br>

| Key（键）      | 类型  | 释义       |
|-------------|-----|----------|
| phrase      | str | 词条名称     |
| placeholder | str | 搜索栏现实的文案 |   