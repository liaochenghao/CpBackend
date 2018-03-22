import random

from rest_framework.response import Response
from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import list_route
from register.models import RegisterInfo, Register, NewCornRecord
from register.serializer import RegisterInfoSerializer, RegisterSerializer, NewCornRecordSerializer
from django.db import transaction
from invitation.models import Invitation
import uuid
import logging

logger = logging.getLogger('django')


class RegisterInfoView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = RegisterInfo.objects.all()
    serializer_class = RegisterInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # 将注册信息录入数据库
        super().create(request, *args, **kwargs)
        # 报名指定的活动
        Register.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                activity_id=request.data.get('activity'))
        # 给新用户添加New币
        NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                     operation=2, corn=20, balance=20)
        return Response()

    def get_queryset(self):
        queryset = super().get_queryset()
        nickname = self.request.query_params.get('nickname')
        wechat = self.request.query_params.get('wechat')
        if nickname:
            queryset = queryset.filter(nickname=nickname)
        if wechat:
            queryset = queryset.filter(wechat=wechat)
        return queryset

    @list_route()
    def random(self, request):
        user_info = request.user_info
        # 首先查询邀请数据表，找到已经邀请的用户的编号
        id_list = Invitation.objects.filter(inviter=user_info['id']).values_list('invitee')
        logger.info('RegisterInfoView random id_list: %s' % id_list)
        # 从注册信息表中随机获取不在已邀请的用户列表中的用户
        total = RegisterInfo.objects.exclude(id__in=list(id_list)).count()
        seed = random.randint(0, total - 1)
        logger.info('RegisterInfoView random seed: %s' % seed)
        result = RegisterInfo.objects.exclude(id__in=id_list)[seed:seed + 1]
        return Response(RegisterInfoSerializer(result[0]).data)


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @list_route(methods=['get'])
    def check_register(self, request):
        """
        检查用户是否已参加活动
        :param request: 
        :return: 
        """
        user_info = request.user_info
        activity_id = request.query_params.get('activity_id')
        if not activity_id:
            raise exceptions.ValidationError('Param activity_id is none')
        result = Register.objects.filter(user_id=user_info.get('user_id'), activity_id=activity_id)
        return Response(True if result else False)


class NewCornRecordView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = NewCornRecord.objects.all()
    serializer_class = NewCornRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @list_route(methods=['get'])
    def statistic(self, request):
        params = request.query_params
        record = NewCornRecord.objects.filter(user_id=params.get('user_id')).latest('create_at')
        serializer = NewCornRecordSerializer(record)
        return Response(serializer.data)
