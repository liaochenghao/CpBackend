### 获检查用户是否关注相关公众号

**请求地址**:
```
    GET     api/v1/register/check_public_number
```

**请求参数**:
```
    {
        type："公众号类型"  0-留学新青年公众号  2-北美留学生公众号
    }
```

**成功返回**：
```
{
    "code": 0,
    "msg": "请求成功",
    "data": {
          true/false
    },
    "field_name": ""
}
```

**失败返回**：
```

```