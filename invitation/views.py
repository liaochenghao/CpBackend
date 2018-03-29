import uuid

import datetime
from django.db import transaction
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from common.ComputeNewCorn import NewCornCompute
from invitation.models import Invitation
from invitation.serializer import InvitationSerializer
import logging

from register.models import RegisterInfo
from register.serializer import RegisterInfoSerializer

logger = logging.getLogger('django')


class InvitationView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        inviter = self.request.query_params.get('inviter')
        invitee = self.request.query_params.get('invitee')
        if inviter:
            queryset = queryset.filter(inviter=inviter)
        if invitee:
            queryset = queryset.filter(invitee=invitee)
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        params = request.data
        user = request.user_info
        if not params.get('invitee'):
            raise serializers.ValidationError('参数 invitee 不能为空')
        super().create(request, *args, **kwargs)
        NewCornCompute.compute_new_corn(user.get('open_id'), 1)
        return Response()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = request.user_info
        status = request.data.get('status')
        if not status or status not in (0, 1, 2):
            logger.info('InvitationView update (status=%s)' % status)
            raise serializers.ValidationError('参数 invitee 有误')
        invitation = Invitation.objects.get(id=pk)
        invitation.status = status
        invitation.save()
        if status == 1:
            NewCornCompute.compute_new_corn(user.get('open_id'), 5)
        return Response()

    @list_route(methods=['get'])
    def cp(self, request, pk):
        result = Invitation.objects.filter(inviter=pk, status=1)
        if not result:
            raise serializers.ValidationError('该用户暂不存在CP')
        invitee = result[0].invitee
        data = RegisterInfo.objects.filter(open_id=invitee).first()
        temp = RegisterInfoSerializer(data).data
        temp['update_at'] = result[0].update_at
        return Response(temp)

    @list_route(methods=['get'])
    def check_inviter(self, request):
        user = request.user_info
        data = Invitation.objects.filter(inviter=user.get('open_id'), status=1)
        return Response(True if data else False)

    @list_route(methods=['get'])
    def check_invitee(self, request):
        user = request.user_info
        data = Invitation.objects.filter(invitee=user.get('open_id'), status=0, expire_at__gt=datetime.datetime.now())
        return Response(True if data else False)
