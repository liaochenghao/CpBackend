# 后台接口文档

### 数据返回格式

**统一为 `json` 格式**:
```
    {
        "code": 0,
        "msg": "success",
        "data": {
            ... // 数据内容
        }
        field_name: ""
    }
```
- code `int` 0为成功，非0为失败 (code=401表示未登录)
- msg `string` 成功或失败的消息
- data `dict` 返回的数据内容
- field_name: `str`  code为非0状态时，报错字段


### API接口文档

**后台接口**:
- [code认证](docs/auth/auth.md)
- [检查账户](docs/auth/check_account.md)
- [获取活动信息](docs/activity/activity.md)
- [填写注册资料](docs/register/register_info.md)
- [随机获取用户信息](docs/register/random_register_info.md)
- [向用户发送邀请](docs/invitation/send_invitation.md)
- [接收用户邀请](docs/invitation/accept_invitation.md)

