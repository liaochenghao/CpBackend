# coding: utf-8
from user_info.models import UserInfo
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['open_id', 'nick_name', 'gender', 'avatar_url', 'city', 'country', 'province', 'create_time',
                  'last_login', 'code', 'cp_user_id', 'cp_time']

    def create(self, validated_data):
        return super().create(validated_data)
