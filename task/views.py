from rest_framework.response import Response
from rest_framework.views import APIView

from CpBackend import settings


class TaskView(APIView):
    def post(self, request):
        f1 = request.FILES['image']
        fname = '%s/upload/task/%s' % (settings.MEDIA_ROOT, f1.name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        return Response()
