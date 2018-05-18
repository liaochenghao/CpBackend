# coding: utf-8
from django.db import models


class UserInfo(models.Model):
    openid = models.CharField('openid', max_length=64, primary_key=True)
    nickname = models.CharField('微信昵称', max_length=64, null=True)
    GENDER = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField('性别', choices=GENDER, default=0)
    avatar_url = models.CharField('用户头像', max_length=255, null=True)
    city = models.CharField('城市', max_length=64, null=True)
    country = models.CharField('国家', max_length=64, null=True)
    province = models.CharField('省份', max_length=64, null=True)
    language = models.CharField('语言', max_length=64, null=True)
    session_key = models.CharField('微信用户标示', max_length=64)
    unionid = models.CharField('unionid', max_length=64, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    code = models.CharField('用户活动码', max_length=16, unique=True)
    qr_code = models.CharField('用户邀请二维码', max_length=255, null=True)
    last_login = models.DateTimeField('最后登录时间', null=True)
    cp_user_id = models.CharField('用户CP编号', max_length=64, null=True)
    cp_time = models.DateTimeField('CP匹配成功时间', null=True)

    class Meta:
        db_table = "user_info"


class TemplateInfo(models.Model):
    """
    小程序模板消息
    """
    id = models.AutoField('序号', primary_key=True)
    template_id = models.CharField('模板ID', max_length=64)
    extra = models.CharField('描述信息', max_length=255)
    type = models.IntegerField('类别标记')
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)

    class Meta:
        db_table = 'template_info'


class UserFormId(models.Model):
    """
    存储form ID
    """
    TYPE_CHOICE = (
        (0, '未使用'),
        (1, '已使用')
    )
    user = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING)
    form_id = models.CharField('FormId', max_length=100)
    type = models.IntegerField('是否使用过', default=0, choices=TYPE_CHOICE)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    expire_time = models.DateTimeField('过期时间', null=True)

    class Meta:
        db_table = 'user_form_id'
        ordering = ['-create_at']
