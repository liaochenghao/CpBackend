# coding: utf-8
from authentication.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nick_name', 'gender', 'head_img_url', 'city', 'country', 'province', 'create_time', 'last_login']



