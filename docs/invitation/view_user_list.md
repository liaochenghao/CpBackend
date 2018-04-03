### 获取已经查看过的用户列表

**请求地址**:
```
    GET     api/v1/user_record/
```

**请求参数**:
```
    {"user_id": "当前用户ID"}
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "user_id": "ohg3z0PZe-POhxYCIaXNm16menX4",
                "view_user_id": "111",
                "create_at": "2018-04-03T10:09:39.964218",
                "invite_status": 0,
                "invite_expire_at": "2018-04-03T10:26:08"
            }
        ]
    },
    "field_name": ""
}
```

**失败返回**：
```

```