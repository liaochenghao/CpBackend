# coding: utf-8
import uuid
from rest_framework import serializers
from invitation.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id', 'inviter', 'invitee', 'create_time', 'status']
        read_only_fields = ['id','inviter',]

