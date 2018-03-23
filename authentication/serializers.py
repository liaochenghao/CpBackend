# coding: utf-8
from authentication.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['open_id', 'nick_name', 'gender', 'avatar_url', 'city', 'country', 'province', 'create_time',
                  'last_login']

    def create(self, validated_data):
        return super().create(validated_data)
