import datetime
from rest_framework import viewsets
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all().order_by('-due')
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        new_task= models.Task.objects.create(
            url= request['url'], 
            project= models.Project.objects.get(id=int(request['project'])),
            dev= models.RegisteredUser.objects.get(id=int(request['dev'])),
            instruction= request['instruction'],
            due= datetime.date(request['year'], request['month'], request['day']))
        new_task.save()
        return Response(self.serializer_class(new_task).data)
        
        
        