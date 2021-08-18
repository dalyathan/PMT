import datetime
from rest_framework import viewsets
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all().order_by('-created')
    serializer_class = serializers.ProjectSerializer
    task_serializer= serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        proj_data= request.data
        new_proj= models.Project.objects.create(sdm= proj_data['sdm'], 
            name= proj_data['name'], manager= request.user)
        new_proj.save()
        new_role= models.Role.objects.create(user= request.user, 
        role= models.Role.UserRole.MANAGER, project= new_proj)
        new_role.save()
        return Response(self.serializer_class(new_proj).data)

    @action(methods=['get'], detail= True)
    def tasksinprogress(self, request, pk):
        return self.status_helper(request, pk, task_status= models.Task.TaskStatus.DOING)

    @action(methods=['get'], detail= True)
    def pendingtasks(self, request, pk):
        return self.status_helper(request, pk, task_status= models.Task.TaskStatus.PENDING)
    
    @action(methods=['get'], detail= True)
    def completedtasks(self, request, pk):
        return self.status_helper(request, pk, task_status= models.Task.TaskStatus.COMPLETED)
    
    @action(methods=['get'], detail= True)
    def rejectedtasks(self, request, pk):
        return self.status_helper(request, pk, task_status= models.Task.TaskStatus.REJECTED)
    
    def status_helper(self, request, pk, task_status):
        try:
            this_proj= models.Project.objects.get(pk=int(pk))
        except models.Project.DoesNotExist:
            return Response('No such Project', status.HTTP_400_BAD_REQUEST)
        if this_proj.manager != request.user:
            return Response("You don't have permission for this", status.HTTP_400_BAD_REQUEST)
        json= self.task_serializer(context={
                'request': request
            },
            instance=this_proj.tasks.filter(status= task_status),many= True)
        return Response(json.data, status.HTTP_200_OK)

    @action(methods=['get'], detail= True)
    def tasksduetoday(self, request, pk):
        today= datetime.datetime.now().strftime("%Y-%m-%d")
        return self.dueness_helper(request, pk, due= today)

    @action(methods=['get'], detail= True)
    def tasksduethisweek(self, request, pk):
        today= datetime.datetime.now().strftime("%Y-%m-%d")
        sunday= datetime.date.today() + datetime.timedelta(days=7 - datetime.datetime.today().isoweekday())
        return self.dueness_helper(request, pk, 
          due__gt= today, due__lte=sunday.strftime("%Y-%m-%d"))
    
    @action(methods=['get'], detail= True)
    def overduetasks(self, request, pk):
        return self.dueness_helper(request, pk, due__lt= datetime.date.today().strftime("%Y-%m-%d"))
    
    def dueness_helper(self, request, pk, **kwargs):
        try:
            this_proj= models.Project.objects.get(pk=int(pk))
        except models.Project.DoesNotExist:
            return Response('No such Project', status.HTTP_400_BAD_REQUEST)
        if this_proj.manager != request.user:
            return Response("You don't have permission for this", status.HTTP_400_BAD_REQUEST)
        json= self.task_serializer(context={
                'request': request
            },
            instance=this_proj.tasks.filter(**kwargs),many= True)
        return Response(json.data, status.HTTP_200_OK)