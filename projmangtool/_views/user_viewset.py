from rest_framework import viewsets
from rest_framework.decorators import action
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response

class RegisteredUserViewSet(viewsets.ModelViewSet):
    queryset = models.RegisteredUser.objects.all().order_by('-date_joined')
    serializer_class = serializers.RegisteredUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'],detail= False)
    def getmyprojs(self, request):
        projs= models.Role.objects.filter(user= request.user)
        print(projs)
        return Response(serializers.
            RoleSerializer( context={
                'request': request
            },
            instance=projs, many= True).data)
