from django.urls import path, include
from rest_framework import routers
from staff.administrator.viewsets.document import DocumentViewSet

router = routers.DefaultRouter()
router.register("document", DocumentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
