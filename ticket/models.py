from django.db import models
from user_info.models import UserInfo


class Ticket(models.Model):
    user = models.ForeignKey(UserInfo)
    ticket = models.CharField('用户ticket', primary_key=True, max_length=100)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    expired_time = models.DateTimeField('过期时间')

    class Meta:
        db_table = "ticket"
