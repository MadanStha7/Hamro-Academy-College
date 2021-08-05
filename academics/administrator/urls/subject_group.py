from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.subject_group import SubjectGroupViewSet

router = routers.DefaultRouter()
router.register("subject_group", SubjectGroupViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
