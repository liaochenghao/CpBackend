# coding: utf-8
from authentication.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['open_id', 'union_id', 'nickname', 'sex', 'city', 'country', 'province', 'head_img_url', 'create_at',
                  'privilege']