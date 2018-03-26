# coding: utf-8
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
    record = NewCornRecord.objects.filter(open_id=user_id)
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
