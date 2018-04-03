import random

import datetime
from rest_framework.response import Response
from rest_framework import mixins, viewsets, exceptions
from rest_framework.decorators import list_route, detail_route
from authentication.models import User
from register.models import RegisterInfo, Register, NewCornRecord
from register.serializer import RegisterInfoSerializer, RegisterSerializer, NewCornRecordSerializer
from django.db import transaction
from invitation.models import Invitation, UserRecord
import uuid
import logging
from common.ComputeNewCorn import NewCornCompute
from common.NewCornType import NewCornType

logger = logging.getLogger('django')


class RegisterInfoView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = RegisterInfo.objects.all()
    serializer_class = RegisterInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user_info
        # 查看当前用户是否已经注册过信息
        record = RegisterInfo.objects.filter(user_id=request.data.get('user'))
        if record:
            raise exceptions.ValidationError('当前用户已经注册过信息')
        # 将注册信息录入数据库
        request.data['id'] = str(uuid.uuid4())
        request.data['user'] = user.get('open_id')
        logger.info('ooooooooooooooooooooooooooooooooooooooooo')
        logger.info(request.data['birthday'])
        request.data['constellation'] = self._get_constellations(request.data['birthday'])
        request.data['avatar_url'] = user.get('avatar_url')
        super().create(request, *args, **kwargs)
        # 报名指定的活动
        Register.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                activity_id=request.data.get('activity'))
        # 给新用户添加New币
        NewCornCompute.compute_new_corn(user.get('open_id'), NewCornType.ATTEND_ACTIVITY.value)
        if request.data.get('invite_code'):
            inviter = User.objects.filter(code=request.data.get('invite_code'))
            if inviter:
                NewCornCompute.compute_new_corn(inviter[0].open_id, NewCornType.INVITE_USERS_ATTEND.value)
        return Response()

    def _get_constellations(self, birthday):
        """
        根据出生日期计算星座
        :param birthday: 
        :return: 
        """
        if not birthday:
            raise exceptions.ValidationError('生日信息不能为空')
        temp = datetime.datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S")
        day = temp.day
        month = temp.month
        dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
        constellations = ("摩羯", "水瓶", "双鱼", "白羊", "金牛", "双子", "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯")
        if day < dates[month - 1]:
            return constellations[month - 1]
        else:
            return constellations[month]

    def get_queryset(self):
        queryset = super().get_queryset()
        nickname = self.request.query_params.get('nickname')
        wechat = self.request.query_params.get('wechat')
        user_id = self.request.query_params.get('user_id')
        if nickname:
            queryset = queryset.filter(nickname=nickname)
        if wechat:
            queryset = queryset.filter(wechat=wechat)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @list_route()
    @transaction.atomic
    def random(self, request):
        user_info = request.user_info
        if request.query_params.get('auto') == 'True':
            NewCornCompute.compute_new_corn(user_info.get('open_id'), NewCornType.SWITCH_USER.value)
        # 首先查询已看过用户记录表
        id_list = UserRecord.objects.filter(user_id=user_info['open_id']).values_list('view_user_id')
        id_result_list = list()
        for _id in id_list:
            id_result_list.append(_id[0])
        # 在查询的时候不能随机获取到当前用户，故需要将当前用户编号放入排他条件中
        id_result_list.append(user_info.get('open_id'))
        logger.info('RegisterInfoView random id_list: %s' % id_result_list)
        # 从注册信息表中随机获取不在已邀请的用户列表中的用户
        total = RegisterInfo.objects.exclude(user_id__in=id_result_list).count()
        if total == 0:
            raise exceptions.ValidationError('暂无匹配用户信息')
        logger.info('RegisterInfoView total = %s' % total)
        seed = random.randint(0, total - 1)
        logger.info('RegisterInfoView random seed: %s' % seed)
        result = RegisterInfo.objects.exclude(user_id__in=id_list)[seed:seed + 1]
        if len(result) == 0:
            raise exceptions.ValidationError('暂无匹配用户信息')
        logger.info('随机获取到的用户ID= %s' % result[0].user_id)
        user = User.objects.filter(open_id=result[0].user_id).first()
        data = RegisterInfoSerializer(result[0]).data
        # 获取到随机用户之后，应将当前用户放入查看记录表user_record中
        UserRecord.objects.create(user_id=user_info['open_id'], view_user_id=data.get('user'))
        data['avatar_url'] = user.avatar_url
        data['age'] = datetime.datetime.now().year - int(data['birthday'][:4])
        data['sex'] = '男' if data['sex'] == 1 else '女'
        if data['demand_cp_age'] == 0:
            data['demand_cp_age'] = '比TA大'
        elif data['demand_cp_age'] == 1:
            data['demand_cp_age'] = '跟TA一样'
        elif data['demand_cp_age'] == 2:
            data['demand_cp_age'] = '比TA小'
        if data['sexual_orientation'] == 0:
            data['sexual_orientation'] = '异性'
        elif data['sexual_orientation'] == 1:
            data['sexual_orientation'] = '同性'
        elif data['sexual_orientation'] == 1:
            data['sexual_orientation'] = '双性'
        if data['overseas_study_status'] == 0:
            data['overseas_study_status'] = '准留学生'
        elif data['overseas_study_status'] == 1:
            data['overseas_study_status'] = '留学生'
        elif data['overseas_study_status'] == 2:
            data['overseas_study_status'] = '毕业生'
        return Response(data)

    def update(self, request, *args, **kwargs):
        result = RegisterInfo.objects.get(id=kwargs.get('pk'))
        params = request.data
        if params.get('nickname'):
            result.nickname = params.get('nickname')
        if params.get('sexual_orientation'):
            result.sexual_orientation = params.get('sexual_orientation')
        if params.get('overseas_study_status'):
            result.overseas_study_status = params.get('overseas_study_status')
        if params.get('wechat'):
            result.wechat = params.get('wechat')
        if params.get('phone_number'):
            result.phone_number = params.get('phone_number')
        if params.get('hometown'):
            result.hometown = params.get('hometown')
        if params.get('future_city'):
            result.future_city = params.get('future_city')
        if params.get('future_school'):
            result.future_school = params.get('future_school')
        result.save()
        return Response()


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
        result = Register.objects.filter(user_id=user_info.get('open_id'), activity_id=activity_id)
        return Response(True if len(result) != 0 else False)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user_info = request.user_info
        # 报名指定的活动
        Register.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                activity_id=request.data.get('activity'))
        # 给新用户添加New币
        NewCornCompute.compute_new_corn(user_info.get('open_id'), NewCornType.ATTEND_ACTIVITY.value)


class NewCornRecordView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = NewCornRecord.objects.all()
    serializer_class = NewCornRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @detail_route(methods=['get'])
    def balance(self, request, pk):
        user_id = pk
        new_corn_record = NewCornRecord.objects.filter(user_id=user_id)
        if not new_corn_record:
            balance = 0
        else:
            new_corn_record = new_corn_record.latest('create_at')
            balance = new_corn_record.balance
        return Response({'user_id': user_id, 'balance': balance})
