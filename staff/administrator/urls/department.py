from django.urls import path, include
from rest_framework import routers
from staff.administrator.viewsets.department import DepartmentViewset

router = routers.DefaultRouter()
router.register("department", DepartmentViewset)

urlpatterns = [
    path("", include(router.urls)),
]
