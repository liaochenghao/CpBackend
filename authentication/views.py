# Create your views here.
import datetime
from rest_framework import mixins, viewsets, exceptions
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
            raise exceptions.ValidationError('Param code is none')
        res = WxInterfaceUtil.code_authorize(code)
        logger.info('Authorize Response : %s' % res.__str__())
        response = Response(res)
        response.set_cookie('ticket', res['ticket'])
        return response

    def create(self, request, *args, **kwargs):
        params = request.data
        user = User.objects.filter(id=params['id']).first()
        user.last_login = datetime.datetime.now()
        user.head_img_url = params['head_img_url']
        user.country = params['country']
        user.province = params['province']
        user.city = params['city']
        user.nick_name = params['nick_name']
        user.gender = params['gender']
        user.save()
        return Response(UserSerializer(user).data)
