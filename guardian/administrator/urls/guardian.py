from django.urls import include, path
from rest_framework import routers

from guardian.administrator.viewsets.guardaininfo import (
    GuardianInfoViewSet,
    StudentGuardianInfoView,
)

router = routers.DefaultRouter()
router.register(r"guardian_info", GuardianInfoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("student_guardian/", StudentGuardianInfoView.as_view()),
]
