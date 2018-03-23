# coding: utf-8
import datetime
import json
import logging
import requests
from rest_framework import exceptions
from CpBackend.settings import WX_SMART_CONFIG
from authentication.models import User
from register.models import NewCornRecord
from ticket.functions import TicketAuthorize

logger = logging.getLogger('django')


class WxInterface:
    def __init__(self):
        self.appid = WX_SMART_CONFIG['appid']
        self.secret = WX_SMART_CONFIG['secret']

    def code_authorize(self, code):
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.get(url=url, params=params)
        if response.status_code != 200:
            logger.info('WxInterface code_authorize response: %s' % response.text)
            raise exceptions.ValidationError('connecting wechat server error')
        res = response.json()
        if res.get('openid') and res.get('session_key'):
            logger.info(res)
            # 首先查询数据库中是否存在该用户信息
            user = User.objects.filter(open_id=res['openid']).first()
            if not user:
                # 如果用户不存在，则向数据库插入数据
                user = User.objects.create(open_id=res['openid'], last_login=datetime.datetime.now(),
                                           session_key=res['session_key'])
                # 同时给用户分配new corn 20
                NewCornRecord.objects.create(user=user, operation=2, corn=20, balance=20)
            else:
                user.last_login = datetime.datetime.now()
                user.save()
            ticket = TicketAuthorize.create_ticket(res['openid'])
            return {'user_id': user.open_id, 'ticket': ticket}
        else:
            logger.info('WxInterface code_authorize response: %s' % response.text)
            raise exceptions.ValidationError('wechat authorize error： %s' % json.dumps(res))


WxInterfaceUtil = WxInterface()
