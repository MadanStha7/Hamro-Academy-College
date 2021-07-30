from django.urls import path, include
from rest_framework import routers
from user.administrator.viewsets.role import RoleViewSet

router = routers.DefaultRouter()
router.register("role", RoleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
