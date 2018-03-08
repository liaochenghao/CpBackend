# coding: utf-8
from activity.models import Activity
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'image_url', 'image_text', 'context', 'register_time', 'activity_time']
