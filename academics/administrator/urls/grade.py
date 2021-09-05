from django.urls import path, include
from rest_framework import routers
from academics.administrator.viewsets.grade import GradeViewSet, GradeListView

router = routers.DefaultRouter()
router.register("grade", GradeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("grade_list/", GradeListView.as_view()),
]
