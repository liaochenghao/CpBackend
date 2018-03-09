from django.db import models


# Create your models here.
class RegisterInfo(models.Model):
    SEX_CHOICE = (
        (0, '异性'),
        (1, '同性'),
        (2, '双性')
    )
    OVERSEAS_STUDY_STATUS = (
        (0, '准留学生'),
        (1, '留学生'),
        (2, '毕业生')
    )
    id = models.CharField('序列号', max_length=64, primary_key=True)
    nickname = models.CharField('活动昵称', max_length=64)
    sexual_orientation = models.IntegerField('性取向', choices=SEX_CHOICE)
    overseas_study_status = models.IntegerField('留学状态', choices=OVERSEAS_STUDY_STATUS)
    wechat = models.CharField('微信号或手机号', max_length=32)
    phone_number = models.CharField('手机号码', max_length=11, null=True)
    hometown = models.CharField('家乡', max_length=64)
    future_city = models.CharField('想就读的城市', max_length=64)
    future_school = models.CharField('想就读的学校', max_length=64)
    create_at = models.DateTimeField('注册时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "register_info"
