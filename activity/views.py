from rest_framework.response import Response
from rest_framework.views import APIView
from activity.models import Activity
from activity.serializers import ActivitySerializer
from rest_framework import exceptions
from register.models import Register
from common.execute_sql import dict_fetchall


class ActivityView(APIView):
    def get(self, request):
        params = request.query_params
        if not params.get('name'):
            raise exceptions.ValidationError('参数name(活动名称)不能为空')
        activity = Activity.objects.filter(name=params.get('name'))
        if not activity:
            raise exceptions.ValidationError('未查询到当前活动信息')
        serializer = ActivitySerializer(activity[0])
        result = serializer.data
        # 查询报名表中报名人数
        user_count = Register.objects.filter(activity=1).count()
        result['user_count'] = user_count
        return Response(result)


class ActivityStartAtView(APIView):
    def get(self, request):
        params = request.query_params
        if not params.get('name'):
            raise exceptions.ValidationError('参数name(活动名称)不能为空')
        activity = Activity.objects.filter(name=params.get('name'))
        if not activity:
            raise exceptions.ValidationError('未查询到当前活动信息')
        serializer = ActivitySerializer(activity[0])
        result = serializer.data
        return Response(result['start_at'])


class TestView(APIView):
    def get(self, request):
        sql = 'SELECT invitee,COUNT(*) as number from invitation GROUP BY invitee'
        result = dict_fetchall(sql)
        print(result)
        return Response(result)
