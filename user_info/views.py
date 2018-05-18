# Create your views here.
import datetime
from django.db import transaction
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.utils import timezone
from CpBackend.settings import WX_SMART_CONFIG
from user_info.models import UserInfo
from user_info.serializers import UserInfoSerializer
from user_info.models import UserFormId
from utils.WXBizDataCrypt import WXBizDataCrypt
from utils.redis_server import redis_client
from utils.weixin_functions import WxInterfaceUtil

from user_info.models import UserInfoDetail
from user_info.serializers import UserInfoDetailSerializer

import logging

logger = logging.getLogger('django')


class UserInfoView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    @list_route(['POST'])
    def authorize(self, request):
        """客户端登录获取授权"""
        code = request.data.get('code')
        if not code:
            raise serializers.ValidationError('Param code is none')
        res = WxInterfaceUtil.code_authorize(code)
        response = Response(res)
        response.set_cookie('ticket', res['ticket'])
        return response

    @list_route(['POST'])
    @transaction.atomic
    def check_account(self, request):
        params = request.data
        encryptedData = params.get('encryptedData')
        session_key = params.get('session_key')
        iv = params.get('iv')
        if not all((iv, encryptedData, session_key)):
            raise serializers.ValidationError('encryptedData、iv、session_key参数不能为空')
        user_info = UserInfo.objects.filter(openid=params.get('openid')).first()
        if not user_info:
            logger.info('系统错误：无法通过用户openid获取用户信息: openid=%s' % params.get('openid'))
            raise serializers.ValidationError('系统错误：无法通过用户openid获取用户信息: openid=%s' % params.get('openid'))
        update_user_tag = False
        if not user_info.unionid:
            update_user_tag = True
            # 如果用户未获取到unionid，则需要解密获取
            data = WXBizDataCrypt(WX_SMART_CONFIG['appid'], user_info.session_key)
            user_data = data.decrypt(encryptedData, iv)
            user_info.unionid = user_data.get('unionId')
            # 给用户初始话费
            # TelephoneChargesCompute.compute_telephone_charges(params.get('openid'), 0, 15, extra='系统初始话费')
        # 录入用户信息到数据库，同时也要注意微信用户可能会更换信息
        if user_info.nickname != params.get('nickname') or user_info.avatar_url != params.get('avatar_url'):
            update_user_tag = True
            user_info.nickname = params.get('nickname')
            user_info.gender = params.get('gender')
            user_info.province = params.get('province')
            user_info.country = params.get('country')
            user_info.city = params.get('city')
            user_info.avatar_url = params.get('avatar_url')
            user_info.language = params.get('language')
        if update_user_tag is True:
            user_info.save()
            temp = UserInfoSerializer(user_info).data
            redis_client.set_instance(user_info.open_id, temp)
            logger.info('更新用户信息: openid=%s' % params.get('openid'))
        return Response()

    @list_route(['POST'])
    def take_form_id(self, request):
        params = request.data
        openid = params.get('openid')
        formid = params.get('formid')
        UserFormId.objects.create(user_id=openid, form_id=formid,
                                  expire_time=datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=+7))
        return Response()


class UserInfoDetailView(mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet
                         ):
    queryset = UserInfoDetail.objects.all()
    serializer_class = UserInfoDetailSerializer


