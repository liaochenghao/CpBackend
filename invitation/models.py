from django.db import models


# Create your models here.
class Invitation(models.Model):
    STATUS = (
        (0, '有效'),
        (1, '成功'),
        (2, '无效')
    )
    id = models.CharField('序列号', max_length=64, primary_key=True)
    inviter = models.CharField('邀请人', max_length=64)
    invitee = models.CharField('被邀请人', max_length=64)
    status = models.IntegerField('状态', choices=STATUS)
    create_time = models.DateTimeField('邀请时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('更新时间', auto_now=True, null=True)

    class Meta:
        db_table = "invitation"
