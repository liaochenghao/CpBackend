# coding: utf-8
import datetime

from register.models import NewCornRecord

OPTION_CHOICE = (
    (0, '关注留学新青年'),
    (1, '邀请用户'),
    (2, '注册成功'),
    (3, '每日登陆'),
    (4, '活动报名'),
    (5, '接受用户邀请'),
    (6, '切换用户'),
)


def compute_new_corn(user_id, operation):
    # 如果是关注公众号或者注册信息，则需要判断数据库中是否存在记录
    if operation == 0 or operation == 2:
        record = NewCornRecord.objects.filter(open_id=user_id)
        corn = 3 if operation == 0 else 20
        if not record:
            NewCornRecord.objects.create(user=user_id, operation=operation, balance=corn, corn=corn)
        else:
            balance = record[0].balance
            NewCornRecord.objects.create(user=user_id, operation=operation, balance=corn + balance, corn=corn)
    if operation == 3:
        now_time = datetime.datetime.now()
        record = NewCornRecord.objects.filter(open_id=user_id, operation=operation, create_at__day=now_time.day)
        if not record:
            balance = record[0].balance
            # 查询最新记录添加记录
            NewCornRecord.objects.create(user=user_id, operation=operation, balance=1 + balance, corn=1)
    if operation == 0 or operation == 1:
        add, corn = True, 2
    elif operation == 2:
        add, corn = True, 3
    if not record:
        NewCornRecord.objects.create(user=user_id, operation=operation, balance=corn)
    else:
        balance = record.balance
        balance = balance + corn if add else balance - corn
        NewCornRecord.objects.create(user=user_id, operation=operation, balance=balance, corn=corn)
