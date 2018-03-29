### 获取CP大神接口

**请求地址**:
```
    GET     api/v1/invitation/cp_god
```

**请求参数**:
```
    
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
         [{
            "user_id": XXX 大神用户编号,
            "avatar_url": "大神头像地址",
            "nickname":"大神昵称",
            "total":"大神受邀次数",
            "invite": 1/0 "当前用户是否邀请过大神"
         },
         {
            "user_id": XXX 大神用户编号,
            "avatar_url": "大神头像地址",
            "nickname":"大神昵称",
            "total":"大神受邀次数",
            "invite": 1/0 "当前用户是否邀请过大神"
         }
         ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```