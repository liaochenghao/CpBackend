# coding: utf-8
from user_info.models import UserInfo
from rest_framework import serializers
from user_info.models import UserInfoDetail
from user_info.function import get_constellation
from datetime import datetime


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['openid', 'nickname', 'gender', 'avatar_url', 'city', 'country', 'province', 'create_at',
                  'last_login', 'code', 'cp_user_id', 'cp_time']

    def create(self, validated_data):
        return super().create(validated_data)


class UserInfoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoDetail
        fields = ['gender', 'sexual', 'birthday', 'status', 'user_id', 'create_at']

    def create(self, validated_data):
        validated_data['user_id'] = self.context.get('request').data['user_id']
        age = datetime.now().year - int(validated_data['birthday'].year)
        validated_data['age'] = age

        validated_data['constellation'] = get_constellation(validated_data['birthday'].month,
                                                            validated_data['birthday'].day)
        return super().create(validated_data)
