from rest_framework import viewsets
from rest_framework.decorators import action
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


class RegisteredUserViewSet(viewsets.ModelViewSet):
    queryset = models.RegisteredUser.objects.all().order_by('-date_joined')
    serializer_class = serializers.RegisteredUserSerializer
    task_serializer= serializers.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'],detail= False)
    def getmyprojs(self, request):
        projs= models.Role.objects.filter(user= request.user)
        return Response(serializers.
            RoleSerializer( context={
                'request': request
            },
            instance=projs, many= True).data)

    @action(methods=['post'], detail= False)
    def leaveteam(self, request):
        try:
            project= models.Project.objects.get(pk= int(request.data['proj']))
        except models.Project.DoesNotExist:
            return Response("The provided project doesn't exist", status.HTTP_400_BAD_REQUEST)
        user_from_db= models.RegisteredUser.objects.get(pk= int(request.user.id))
        my_tasks= project.tasks.filter(dev= user_from_db)
        for task in my_tasks:
            print(task)
            task.status= models.Task.TaskStatus.REJECTED
            task.save()
        return Response('Done', status.HTTP_200_OK)
    
    @action(methods=['get'], detail= True)
    def getassignedtasks(self, request, pk):
        return Response(self.task_serializer(context={
                'request': request
            },
            instance=request.user.my_tasks.exclude(status= models.Task.TaskStatus.REJECTED), 
            many= True).data)

        
