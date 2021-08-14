"""backtools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from projmangtool._views.user_viewset import RegisteredUserViewSet
from projmangtool._views.task_viewset import TaskViewSet
from projmangtool._views.role_viewset import RoleViewSet
from projmangtool._views.proj_viewset import ProjectViewSet
from projmangtool import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name= 'projmangtool'

router = routers.DefaultRouter()
router.register(r'users', RegisteredUserViewSet)
router.register(r'projs', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('', include('authemail.urls')), #views.RegisterView.as_view(), name='auth_register'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
