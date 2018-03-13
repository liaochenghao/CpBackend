# coding: utf-8
import datetime

from authentication.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        # read_only_fields = ['id']

    def create(self, validated_data):
        user, created = User.objects.get_or_create(id=validated_data['id'])
        user.last_login = datetime.datetime.now()
        user.save()

