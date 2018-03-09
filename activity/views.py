from rest_framework.response import Response
from rest_framework.views import APIView
from activity.models import Activity
from activity.serializers import ActivitySerializer
from rest_framework import exceptions


class ActivityView(APIView):
    def get(self, request):
        params = request.query_params
        if not params.get('name'):
            raise exceptions.ValidationError('Param activity name is None')
        activity = Activity.objects.filter(name=params.get('name')).first()
        if not activity:
            raise exceptions.ValidationError('Can not find activity information')
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)
