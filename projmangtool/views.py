from rest_framework.decorators import action
from . import models,serializers
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .serializers import MyTokenObtainPairSerializer,RegisteredUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
# Create your views here.
class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'signup':
                return True
            else:
                return False
        else:
            return True

class RegisterView(generics.CreateAPIView):
    queryset = models.RegisteredUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisteredUserSerializer
    
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

