# coding: utf-8
from rest_framework import serializers

from ticket.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField()

    class Meta:
        model = Ticket
        fields = ['user', 'ticket', 'create_time', 'expired_time']
