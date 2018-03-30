from django.db import models

# Create your models here.
from authentication.models import User


class Task(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    name = models.CharField('任务名称', max_length=64)

    extra = models.CharField('备注', max_length=255, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "task"
        ordering = ['-create_at']


class UserTask(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    status = models.IntegerField('任务状态')
    extra = models.CharField('备注', max_length=255, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "user_task"
        ordering = ['-create_at']
