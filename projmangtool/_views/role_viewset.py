from rest_framework import viewsets
from projmangtool import models,serializers
from rest_framework import permissions
from rest_framework.response import Response

class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [permissions.IsAuthenticated]