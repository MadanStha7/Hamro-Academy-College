from django.urls import include, path
from rest_framework import routers
from fees.administrator.viewsets.fine_type import FineTypeViewSet

router = routers.DefaultRouter()
router.register(r"fine_type", FineTypeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
