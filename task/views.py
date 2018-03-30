from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from common.execute_sql import execute_custom_sql

from CpBackend import settings
from task.models import Task, UserTask
from task.serializer import TaskSerializer


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
        pass


# f1 = request.FILES['image']
# fname = '%s/upload/task/%s' % (settings.MEDIA_ROOT, f1.name)
# with open(fname, 'wb') as pic:
#     for c in f1.chunks():
#         pic.write(c)
# return Response()


class UserTaskContentView(APIView):
    def post(self, request):
        pass
