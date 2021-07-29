from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.class_viewset import ClassViewSet


router = routers.DefaultRouter()
router.register("class", ClassViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
