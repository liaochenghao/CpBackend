from django.db.models import Q
import uuid
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from CpBackend import settings
from task.models import Task, UserTask
from task.serializer import TaskSerializer, UserTaskSerializer, User


class TaskView(APIView):
    def get(self, request):
        """
        获取当前用户任务列表
        :param request: 
        :return: 
        """
        user = request.user_info
        query_set = Task.objects.all()
        all_task = TaskSerializer(query_set, many=True).data
        task_ids = list()
        for task in all_task:
            task_ids.append(task['id'])
        user_task_infos = UserTask.objects.filter(Q(user_id=user.get('open_id')) | Q(cp_user_id=user.get('open_id')),
                                                  task_id__in=task_ids).values('task_id', 'status')
        for task in all_task:
            task['attend'] = False
            for info in user_task_infos:
                if task['id'] == info['task_id']:
                    task['attend'] = True
                    task['status'] = info['status']
                    break
        return Response(all_task)

    def post(self, request):
        f1 = request.FILES['image']
        fname = '%s/upload/task/%s' % (settings.MEDIA_ROOT, f1.name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        return Response()


class UserTaskView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer

    def create(self, request, *args, **kwargs):
        param = request.data
        if not param.get('task_id'):
            raise serializers.ValidationError('参数task_id不能为空')
        user = request.user_info
        # 首先判断当前用户是否有CP，如果有CP，则一定查询到2条记录，否则0条记录
        cp_result = User.objects.filter(
            Q(cp_user_id=user.get('open_id')) | Q(open_id=user.get('open_id', cp_user_id__isnull=False)))
        if not cp_result:
            raise serializers.ValidationError('当前用户暂无CP信息')
        cp_user_id = cp_result[0].cp_user_id if cp_result[0].open_id == user.get('open_id') else cp_result[1].open_id
        UserTask.objects.create(id=str(uuid.uuid4()), task_id=param.get('task_id'), user_id=user.get('open_id'),
                                cp_user_id=cp_user_id)
        return Response("任务领取成功")

    def update(self, request, *args, **kwargs):
        user = request.user_info
        task_id = kwargs.get('pk')
        content = request.data.get('content')
        if not content:
            raise serializers.ValidationError('参数content不能为空')
        user_task = UserTask.objects.filter(Q(user_id=user.get('open_id')) | Q(cp_user_id=user.get('open_id')),
                                            task_id=task_id)
        if not user_task:
            raise serializers.ValidationError('当前用户没有领取该任务')
        user_task[0].extra = content
        user_task[0].save()
        return Response()

    @list_route(methods=['get'])
    def check_cp_task(self):

        return Response()
