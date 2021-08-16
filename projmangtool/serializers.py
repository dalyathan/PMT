from . import models
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token

class RegisteredUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= models.RegisteredUser
        fields= ['id','first_name','last_name','email','password','occupation']

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= models.Project
        fields= ['id','name','sdm']
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= models.Task
        fields= ['id','url','project','dev','instruction','status','due']

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= models.Role
        fields= ['id','user','role','project']