from django.urls import include, path
from rest_framework import routers

from student.administator.viewsets.category import StudentCategoryViewSet


router = routers.DefaultRouter()
router.register(r"student_category", StudentCategoryViewSet)

urlpatterns = [path("", include(router.urls))]
