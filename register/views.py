from rest_framework import mixins, viewsets
import uuid
from register.models import RegisterInfo, Register
from register.serializer import RegisterInfoSerializer, RegisterSerializer


class RegisterInfoView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = RegisterInfo.objects.all()
    serializer_class = RegisterInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        Register.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                activity_id=request.data.get('activity'))

    def get_queryset(self):
        queryset = super().get_queryset()
        nickname = self.request.query_params.get('nickname')
        wechat = self.request.query_params.get('wechat')
        if nickname:
            queryset = queryset.filter(nickname=nickname)
        if wechat:
            queryset = queryset.filter(wechat=wechat)
        return queryset


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
