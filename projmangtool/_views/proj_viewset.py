from rest_framework import viewsets
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all().order_by('-created')
    serializer_class = serializers.ProjectSerializer
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