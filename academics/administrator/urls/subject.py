from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.subject import SubjectViewSet


router = routers.DefaultRouter()
router.register("subject", SubjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
