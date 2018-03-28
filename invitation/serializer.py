# coding: utf-8
from rest_framework import serializers
from invitation.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'inviter', 'invitee', 'create_time', 'status', 'update_at', 'expire_at']
        read_only_fields = ['id', 'inviter', 'expire_at']

    def create(self, validated_data):
        print('3333333333333336666666666666')
        validated_data['expire_at'] = validated_data['create_time']
        print(type(validated_data['expire_at']))
