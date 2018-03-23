# coding: utf-8
import datetime
import json
import logging
import requests
from rest_framework import exceptions
from CpBackend.settings import WX_SMART_CONFIG
from authentication.models import User
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
            user, created = User.objects.get_or_create(open_id=res['openid'])
            user.last_login = datetime.datetime.now()
            user.session_key = res['session_key']
            user.save()
            ticket = TicketAuthorize.create_ticket(res['openid'])
            return {'user_id': user.open_id, 'ticket': ticket}
        else:
            logger.info('WxInterface code_authorize response: %s' % response.text)
            raise exceptions.ValidationError('wechat authorize error： %s' % json.dumps(res))


WxInterfaceUtil = WxInterface()
