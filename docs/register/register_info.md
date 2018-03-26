### 注册用户信息接口

**请求地址**:
```
    GET     api/v1/user_info/
```

**请求参数**:
```
    {
        "nickname":"zhangsan",        活动昵称
        "sexual_orientation":1,       性取向
        "overseas_study_status":1,    留学状态
        "wechat":"bobowang_2018",     微信号
        "phone_number":"15926215673", 手机号
        "hometown":"wuhan",           国内居住城市
        "future_city":"niuyue",       期望就读城市
        "future_school":"havid",      期望就读学校
        "user":"111",                 用户编号（open_id）
        "activity":"1"                活动编号
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
             
    },
    "field_name": ""
}
```

**失败返回**：
```

```