# Create your views here.
from rest_framework import mixins, viewsets
from authentication.models import User
from authentication.serializers import UserSerializer


class UserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
