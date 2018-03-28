# coding: utf-8
import uuid

import datetime
from rest_framework import serializers
from invitation.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'inviter', 'invitee', 'create_time', 'status', 'update_at', 'expire_at']
        read_only_fields = ['id', 'inviter', 'expire_at', 'status']

    def create(self, validated_data):
        validated_data['id'] = str(uuid.uuid4())
        validated_data['inviter'] = self.context.get('request').user_info.get('open_id')
        validated_data['create_time'] = datetime.datetime.now()
        validated_data['expire_at'] = validated_data['create_time'] + datetime.timedelta(days=3)
        validated_data['status'] = 0
        return super().create(validated_data)
