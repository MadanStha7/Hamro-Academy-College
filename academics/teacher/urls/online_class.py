from django.urls import path, include
from rest_framework import routers

from academics.teacher.viewsets.online_class import OnlineClassInfoViewSet

router = routers.DefaultRouter()
router.register(r"online_class", OnlineClassInfoViewSet)

urlpatterns = [path("", include(router.urls))]
