from django.urls import path, include
from rest_framework import routers
from staff.administrator.viewsets.document import StaffDocumentViewSet

router = routers.DefaultRouter()
router.register("staff-documents", StaffDocumentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
