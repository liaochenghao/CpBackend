# coding: utf-8
import datetime
import json

import requests
from rest_framework import exceptions
from CpBackend.settings import WX_SMART_CONFIG
from authentication.models import User
from ticket.functions import TicketAuthorize


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
            raise exceptions.ValidationError('connecting wechat server error')
        res = response.json()
        if res.get('openid') and res.get('session_key'):
            user, created = User.objects.get_or_create(username=res['openid'])
            user.last_login = datetime.datetime.now()
            user.session_key = res['session_key']
            user.save()
            ticket = TicketAuthorize.create_ticket(user.id)
            return {'user_id': user.id, 'ticket': ticket}
        else:
            raise exceptions.ValidationError('wechat authorize error： %s' % json.dumps(res))


WxInterfaceUtil = WxInterface()
