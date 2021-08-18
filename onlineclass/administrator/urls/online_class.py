from django.urls import path, include
from rest_framework import routers
from onlineclass.administrator.viewsets.online_class import OnlineClassViewSet


router = routers.DefaultRouter()
router.register("online_class", OnlineClassViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
