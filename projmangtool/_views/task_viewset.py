import datetime
from django.db.models.base import Model
from rest_framework import viewsets
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
import subprocess
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all().order_by('-due')
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        task_data= request.data
        if self.isGitRepo(task_data['url']):
            return Response("The repo provided doesn't exist", status.HTTP_400_BAD_REQUEST)
        try:
            project= models.Project.objects.get(id=int(task_data['project']))
            developer= models.Project.objects.get(id=int(task_data['project']))
        except models.Project.DoesNotExist:
            return Response('There is no such project', status.HTTP_400_BAD_REQUEST)
        except models.Project.DoesNotExist:
            return Response('There is no such developer', status.HTTP_400_BAD_REQUEST)
        new_task= models.Task.objects.create(
            url= task_data['url'], 
            project= project,
            dev= developer,
            instruction= task_data['instruction'],
            due= datetime.date(int(task_data['year']), int(task_data['month']), int(task_data['day'])))
        new_task.save()
        return Response(self.serializer_class(
            context={
                'request': request
            },
            instance=new_task).data)
    
    def isGitRepo(self, url):
        process= subprocess.run(['git','ls-remote',url])
        return process.returncode != 0
    
    @action(methods=['post'], detail= False)
    def updatestatus(self, request):
        #status either 1= SUBMITTED, 3= DOING, 4= REJECTED for dev
        task= request.data
        if int(task['status']) > 4 or int(task['status']) == 2 :
            return Response('unexpected status id='+task['status']+' provided', status.HTTP_400_BAD_REQUEST)
        if not self.is_task_assigned_to_user(request):
            return Response('You are not assigned to this task', status.HTTP_400_BAD_REQUEST)
        try:
            updated_task= models.Task.objects.get(pk= int(task['id']))
        except models.Task.DoesNotExist:
             return Response('No such task', status.HTTP_400_BAD_REQUEST)
        updated_task.status= models.Task.TaskStatus.values[int(task['status'])]
        updated_task.save()
        self.updaterole(request)
        return Response('Task Status Updated', status.HTTP_200_OK)

    @action(methods=['post'], detail= False)
    def approvetask(self, request):
        #task: int
        #check whether this is the manager of the project
        try:
            task_from_db= models.Task.objects.get(pk= int(request.data['task']))
        except models.Task.DoesNotExist:
            return Response('No such task', status.HTTP_400_BAD_REQUEST)
        if task_from_db.project.manager == request.user:
            print(task_from_db.project.manager)
            if task_from_db.status == models.Task.TaskStatus.REJECTED:
                return Response('This task has been declined by the developer', status.HTTP_400_BAD_REQUEST)
            elif task_from_db.status != models.Task.TaskStatus.SUBMITTED:
                return Response('Task not completed yet', status.HTTP_400_BAD_REQUEST)
            else:
                task_from_db.status= models.Task.TaskStatus.COMPLETED
                return Response('Task Status Updated', status.HTTP_200_OK)
        else:
            return Response('You dont have permission for this', status.HTTP_400_BAD_REQUEST)

    def updaterole(self, request):
        """Update role of developer if this is the only task in this project"""
        task_data= request.data
        task_from_db= models.Task.objects.get(pk= int(task_data['id']))
        how_many_tasks= len(models.Task.objects.filter(project= task_from_db.project, dev= request.user))
        if how_many_tasks == 1 and  task_data['status'] == '4':
            models.Role.objects.filter(project= task_from_db.project, user= request.user).delete()
        if how_many_tasks == 1 and  task_data['status'] == '3':
            new_role= models.Role.objects.create(
                user= request.user, role= models.Role.UserRole.DEVELOPER, project= task_from_db.project)
            new_role.save()
    
    def is_task_assigned_to_user(self, request):
        """checks whether this task is assigned to this user"""
        task_data= request.data
        task_from_db= models.Task.objects.get(pk= int(task_data['id']))
        return task_from_db.dev == request.user
    
    def haspermission(self, request):
        """Checks wether current user has permission to access this task"""
        pass

        
        
        