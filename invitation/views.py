from rest_framework import mixins, viewsets, serializers
from rest_framework.response import Response

from invitation.models import Invitation
from invitation.serializer import InvitationSerializer


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

    def create(self, request, *args, **kwargs):
        params = request.data
        user = request.user_info
        if not params.get('invitee'):
            raise serializers.ValidationError('参数 invitee 不能为空')
        Invitation.objects.create(inviter=user.get('id'), invitee=params.get('invitee'), status=0)
        return Response()

    def update(self, request, *args, **kwargs):
        return Response()
