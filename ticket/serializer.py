# coding: utf-8
from rest_framework import serializers

from user_info.serializers import UserInfoSerializer
from ticket.models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['user', 'ticket', 'create_time', 'expired_time']
        read_only_fields = ['user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserInfoSerializer(instance=instance.user).data
        return data
