# Create your views here.
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer
from utils.weixin_functions import WxInterfaceUtil
import logging

logger = logging.getLogger('django')


class UserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(['GET'])
    def authorize(self, request):
        """客户端登录获取授权"""
        code = request.query_params.get('code')
        if not code:
            raise serializers.ValidationError('Param code is none')
        res = WxInterfaceUtil.code_authorize(code)
        response = Response(res)
        response.set_cookie('ticket', res['ticket'])
        return response

    @list_route(['POST'])
    def check_account(self, request):
        """
        检查用户信息
        :param request: 
        :return: 
        """
        params = request.data
        user = User.objects.filter(open_id=params.get('user_id')).first()
        if not user:
            logger.info('无法通过用户open_id获取用户记录: user_id=%s' % params.get('user_id'))
            raise serializers.ValidationError('无法通过用户open_id获取用户记录: user_id=%s' % params.get('user_id'))
        # 录入用户信息到数据库，同时也要注意微信用户可能会更换信息
        user.nick_name = params.get('nick_name')
        user.gender = params.get('gender')
        user.province = params.get('province')
        user.country = params.get('country')
        user.city = params.get('city')
        user.avatar_url = params.get('avatar_url')
        user.language = params.get('language')
        user.save()
        return Response()
