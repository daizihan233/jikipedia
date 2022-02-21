## **_jikipedia_**
注意：该项目还在开发完善中，有Bug欢迎反馈<br>
注意：请一定要保持更新，否则会导致某些功能失效
### 相关页面导航栏
[小鸡词典 Jikipedia](https://jikipedia.com/) <br>
[作者主页 @Bug鸡](https://jikipedia.com/definitions/user/281250396) <br>
[Github项目](https://github.com/daizihan233/jikipedia)

### 做了些什么？
#### 互动类
- [x] 签到
- [ ] 补签
- [ ] 收藏
- [ ] 新建收藏夹
- [x] 点赞 / 取消点赞
- [ ] 评论 / 回复
- [ ] 关注 / 取消关注
#### 数据类
- [x] 生成XID
- [x] 加密XID
- [x] Token获取
- [ ] 被阅读、点赞的数据
- [ ] 个人信息
- [ ] 关注（者）
- [ ] 粉丝（者）
- [ ] 词条内容
- [ ] 词条编写者
- [x] 搜索栏的推荐
- [ ] 获取昵称
- [ ] 获取头像
- [ ] 获取签名
#### 创作类
- [ ] 创建词条
- [ ] 创建杂谈
#### 活动类
- [x] 恶魔鸡翻译器
### 食用教程
#### 安装
```
pip install jikipedia==0.2.5rc0
```
#### import
```
from jikipedia import Jikipedia
```
如果出现ImportError，请检查是否安装了requests、json、re。
#### 初始化
```
jiki = Jikipedia(phone='12345678901', password='123456')
```
phone 是 11 位手机号，password 是 密码，均为 str 类型。
#### 生成明文XID
```
xid = jiki.generate_plaintext_xid()
```
xid 为 str 类型，可以直接使用。
#### 生成密文XID
```
xid = jiki.encode_xid()
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

| Key（键）      | 类型  | 释义              |
|-------------|-----|-----------------|
| phrase      | str | 搜索栏在被点击时显示的的文案  |            |
| placeholder | str | 搜索栏在没有点击时显示的的文案 |   
#### 点赞 / 取消点赞
```
jiki.like(id, True)
```
id 为 int 类型，True 为点赞，False 为取消点赞。
返回值为其返回的HTTP状态码。
#### 签到
```
jiki.sign()
```